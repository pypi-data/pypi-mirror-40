# -*- coding=utf-8 -*-
import re
import sys
import unittest

from django.conf import settings
from django.test.runner import reorder_suite, DiscoverRunner
from datetime import datetime

WITH_HTML_REPORT = getattr(settings, 'TEST_HTML_REPORT', False)
if WITH_HTML_REPORT:
    try:
        from pyunitreport import HTMLTestRunner
        from ttoolly.html_report.report import CustomHtmlTestResult
    except ImportError:
        raise Exception('For html reports you should install pyunitreport:\n    pip install PyUnitReport')


def get_runner():
    test_runner_class = getattr(settings, 'TEST_RUNNER_PARENT', None)
    if not test_runner_class:
        return DiscoverRunner

    test_path = test_runner_class.split('.')
    test_module = __import__('.'.join(test_path[:-1]), {}, {}, str(test_path[-1]))
    test_runner = getattr(test_module, test_path[-1])
    return test_runner


ParentRunner = get_runner()


class RegexpTestSuiteRunner(ParentRunner):
    parallel = 1
    test_runner = HTMLTestRunner if WITH_HTML_REPORT else ParentRunner.test_runner

    mro_names = [m.__name__ for m in ParentRunner.__mro__]

    def __init__(self, *args, **kwargs):
        super(RegexpTestSuiteRunner, self).__init__(*args, **kwargs)
        self.priority_tags = kwargs['priority_tags']

    @classmethod
    def add_arguments(cls, parser):
        super(RegexpTestSuiteRunner, cls).add_arguments(parser)
        parser.add_argument(
            '--priority-tag', action='append', dest='priority_tags',
            help='Run only tests with the specified tag. Can be used multiple times. If method has tag, not compare class tag.',
        )

    def get_resultclass(self):
        if WITH_HTML_REPORT:
            return CustomHtmlTestResult
        return super(RegexpTestSuiteRunner, self).get_resultclass()

    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        real_parallel = self.parallel
        self.parallel = 1
        full_suite = super(RegexpTestSuiteRunner, self).build_suite(None, extra_tests=None, **kwargs)
        my_suite = unittest.TestSuite()
        labels_for_suite = []
        if test_labels:
            full_re = []
            for label in test_labels:
                if re.findall(r'(^[\w\d_]+(?:\.[\w\d_]+)*$)', label) == [label]:
                    labels_for_suite.append(label)
                    continue
                text_for_re = label.replace('.', '\.').replace('*', '[^\.]+?')
                if 'DiscoverRunner' in self.mro_names:
                    if len(label.split('.')) > 3:
                        text_for_re += '$'
                    else:
                        text_for_re += '\..+$'
                full_re.append(text_for_re)
            full_re = '(^' + ')|(^'.join(full_re) + ')' if full_re else ''
            for el in full_suite._tests:
                module_name = el.__module__

                full_name = [module_name, el.__class__.__name__, el._testMethodName]
                full_name = '.'.join(full_name)
                if (full_re and re.findall(r'%s' % full_re, full_name)):
                    my_suite.addTest(el)
        if labels_for_suite:
            my_suite.addTests(ParentRunner.build_suite(self, labels_for_suite, extra_tests=None, **kwargs))

        if self.priority_tags:
            filter_tests_by_priority_tags(my_suite, self.priority_tags)
        suite = reorder_suite(my_suite, (unittest.TestCase,))

        self.parallel = real_parallel
        if self.parallel > 1:
            parallel_suite = self.parallel_test_suite(suite, self.parallel, self.failfast)

            # Since tests are distributed across processes on a per-TestCase
            # basis, there's no need for more processes than TestCases.
            parallel_units = len(parallel_suite.subsuites)
            if self.parallel > parallel_units:
                self.parallel = parallel_units

            # If there's only one TestCase, parallelization isn't needed.
            if self.parallel > 1:
                suite = parallel_suite

        return suite

    def run_suite(self, suite, **kwargs):
        if WITH_HTML_REPORT:
            resultclass = self.get_resultclass()
            result = self.test_runner(
                output=getattr(settings, 'TEST_REPORT_OUTPUT_DIR', datetime.now().strftime('%Y-%m-%d %H-%M-%S')),
                verbosity=self.verbosity,
                failfast=self.failfast,
                resultclass=resultclass,
            ).run(suite)
        else:
            result = super(RegexpTestSuiteRunner, self).run_suite(suite, **kwargs)
        if self.verbosity > 2 and (result.errors or result.failures):
            st = unittest.runner._WritelnDecorator(sys.stderr)
            st.write('\n' + '*' * 29 + ' Run failed ' + '*' * 29 + '\n\n')
            st.write('python manage.py test %s' % ' '.join(
                ['.'.join([test.__class__.__module__, test.__class__.__name__, test._testMethodName]) for test, _ in
                 result.errors + result.failures]) + '\n\n')
            st.write('*' * 70 + '\n\n')
        return result


def filter_tests_by_priority_tags(suite, tags):
    suite_class = type(suite)
    filtered_suite = suite_class()

    for test in suite:
        if isinstance(test, suite_class):
            filtered_suite.addTests(filter_tests_by_priority_tags(test, tags))
        else:
            test_tags = set(getattr(test, 'tags', set()))
            test_fn_name = getattr(test, '_testMethodName', str(test))
            test_fn = getattr(test, test_fn_name, test)
            test_fn_tags = set(getattr(test_fn, 'tags', set()))
            """if test has tags, not use class tags"""
            all_tags = test_fn_tags or test_tags
            matched_tags = all_tags.intersection(tags)
            if (matched_tags or not tags):
                filtered_suite.addTest(test)

    return filtered_suite

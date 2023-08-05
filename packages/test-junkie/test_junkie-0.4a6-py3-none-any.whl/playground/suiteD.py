import time

from playground.suiteB import TestSuiteB
from test_junkie.decorators import Suite, test, beforeClass, beforeTest, afterTest, afterClass
from test_junkie.meta import meta, Meta
from tests.junkie_suites.TestListener import TestListener
from playground.SpecialDecorators import TestRules


@Suite(retry=2,
       listener=TestListener,
       meta=meta(name="Suite D",
                 known_bugs=[]),
       parameters=[1, 2, 3],
       priority=2, pr=[TestSuiteB], feature="Login", owner="Mike")
class API(TestRules):

    @beforeClass()
    def before_class1(self):
        pass

    @beforeTest()
    def before_test2(self):
        # write your code here
        pass

    @afterTest()
    def after_test3(self):
        # write your code here
        pass

    @afterClass()
    def after_class4(self):
        # write your code here
        pass

    @test(tags=["bom_account_api", "bom"], owner="Artur")
    def a(self, suite_parameter):
        pass
        # raise AssertionError("derp")

    @test(component="OAuth", tags=["bom_domain_api", "bom"])
    def b(self):
        pass
        # raise AssertionError("double derp")

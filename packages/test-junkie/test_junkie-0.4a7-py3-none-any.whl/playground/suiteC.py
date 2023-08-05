import time

from playground.suiteB import TestSuiteB
from test_junkie.decorators import Suite, test, beforeClass, beforeTest, afterTest, afterClass
from test_junkie.meta import meta, Meta
from tests.junkie_suites.TestListener import TestListener
from playground.SpecialDecorators import TestRules


@Suite(retry=2,
       listener=TestListener,
       meta=meta(name="Suite C",
                 known_bugs=[]),
       parameters=[1, 2],
       parallelized=False)
class TestSuiteC(TestRules):

    @test(tags=["bom_account_api", "bom"], owner="Victor")
    def a(self):
        time.sleep(3)

    @test(tags=["bom_user_api", "bom"], owner="Mike")
    def b(self):
        time.sleep(3)

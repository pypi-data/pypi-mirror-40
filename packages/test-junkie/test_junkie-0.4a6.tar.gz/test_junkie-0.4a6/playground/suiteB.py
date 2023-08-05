import time
from test_junkie.decorators import Suite, test
from tests.junkie_suites.TestListener import TestListener


@Suite(retry=2,
       listener=TestListener,
       meta={"name": "Suite B", "known_bugs": []},
       parameters=[1, 2], priority=1, feature="Login",
       owner="George")
class TestSuiteB:

    @test(priority=2, tags=["bom_domain_api", "bom"])
    def a(self):
        time.sleep(2)
        print("Finished SUITE B / TEST A")

    @test(priority=1, tags=["bom_account_api", "bom"])
    def b(self):
        time.sleep(2)
        print("Finished SUITE B / TEST B")

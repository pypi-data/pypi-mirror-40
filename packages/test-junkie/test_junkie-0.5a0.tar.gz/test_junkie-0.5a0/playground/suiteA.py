import time
from test_junkie.decorators import Suite, test, beforeTest
from test_junkie.meta import Meta


def test_func():
    print("evaluating...")
    time.sleep(2)
    return [1, 2]


@Suite(retry=2, feature="Login", owner="Mike", parameters=["1122222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222", 22])
class LoginSuite:

    @beforeTest()
    def before_test(self):
        print("Winning!")

    @test(component="Login Page", skip_before_test=True,
          tags=["positive_flow", "ui", "auth"])
    def positive_login(self):
        time.sleep(1)

    @test(priority=1, skip_before_test=True,
          parallelized_parameters=True,
          component="Login Page",
          tags=["negative_flow", "ui"],
          parameters=[1, 2, 3])
    def negative_login(self, parameter, suite_parameter):
        # time.sleep(3.3)
        raise AssertionError("Missing error message on negative login attempt: {}".format(parameter))

    @test(component="Session", owner="Victor", skip_before_test=True,
          tags=["positive_flow", "ui", "auth", "session"])
    def session_timeout_after_2h(self):
        pass

    @test(component="Session", owner="Victor",
          tags=["positive_flow", "ui", "auth", "session"])
    def session_timeout_after_1h(self):
        pass

    @test(component="Session", owner="Victor",
          tags=["negative_flow", "ui", "auth", "session"])
    def logout_after_session_timeout(self):
        pass

    @test(component="Login Page", skip_before_test=True,
          tags=["negative_flow", "ui"])
    def negative_login_attempt_limit(self):
        # time.sleep(7.3)
        pass
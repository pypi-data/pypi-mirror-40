import time
from test_junkie.decorators import Suite, test
from test_junkie.meta import Meta


def test_func():
    print("evaluating...")
    time.sleep(2)
    return [1, 2]


@Suite(retry=2, parameters=test_func)
class Login:

    # @test()
    # def positive_login(self):
    #     time.sleep(1)

    @test(priority=1,
          parallelized_parameters=True)
    def negative_login(self):
        time.sleep(3.3)
        assert 1 == 2, "Missing error message on negative login attempt: {}".format(None)

    # @test(parameters=[1, 2, 3, 4, 5, 6, 7, 8, 9])
    # def c(self, parameter):
    #     # time.sleep(15)
    #     print("Finished SUITE A / TEST C: Param: ", parameter)

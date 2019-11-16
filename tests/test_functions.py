from slim4py.slim import Slim

if __name__ == '__main__':

    slim = Slim("slim")

    def say_hello():
        return "Hello World"

    print(slim.render("example_functions.slim", say_hello=say_hello, year="2019", author="https://github.com/multiversecoder/slim4py"))

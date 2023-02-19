DESCRIPTION:

Mathyfy is a Python package that can take a string as input and parse it into a python dictionary, (and if you want a JSON math file). The package can parse and evaluate expressions using the operations and objects injected by the user.

WHY DOES THIS EXIST?

I have created a package for General Relativistic calculations, and needed a general purpose language which was scalable for any future mathematical operation and would easily allow me to store user inputs in a database such as CosmosDB/MongoDB. 

CURRENT FEATURES:

1. `Mathyfy`: Will parse a string and return a Python dictionary representing the equation.
2. `MathInterpreter`: Will evaluate the python dictionary based on the injected objects entered by the user that handle the operations. Or on the default operation pre-defined classes.

FUTURE FEATURES:

Ability to execute and interpret the math JSON file by injecting a config object.
A lexer will be implemented to parse latex code.
Bugs will be fixed.

HOW TO USE:

Import Mathyfy into your Python code.
Enter an equation as a string, for example: `Mathify('2+4*7')()`.
Use Mathyfy to convert the string into a dictionary, such as:
```
{
    "operation": "ADD",
    "arguments": [
        {
            "operation": "BUILD_INT",
            "arguments": "2"
        },
        {
            "operation": "MULTIPLY",
            "arguments": [
                {
                    "operation": "BUILD_INT",
                    "arguments": "4"
                },
                {
                    "operation": "BUILD_INT",
                    "arguments": "7"
                }
            ]
        }
    ]
}
```
The structure here is always consistent with:
```
{
    "operation" : "OPERATION",
    "argument"  : [LIST of STRINGS ARGUMENT] or "STRING ARGUMENT"
}
```
You can store this dictionary or use the built-in evaluate method to evaluate the expression with the components you want.
To use the evaluate method, enter a dictionary with the classes that will handle the corresponding arguments. The default operation classes are:
```
DEFAULT_OPERATION_CLASSES = {
"BUILD_INT" : Int,
"BUILD_FLOAT" : Float,
"ADD": Add,
"MULTIPLY": Multiply,
"DIVISION": Division
}
```
The Multiply class is responsible for handling the "MULTIPLY" operation. These are the build in default classes. 

INJECTING YOUR OWN OPERATIONS:

You can however overide how the Evaluate class handles each of the arguments, such as:

String: 
```Mathify('diff(x**2, x) + g_{mu}_{nu}')()```

Output:
```
{
    "operation": "ADD",
    "arguments": [
        {
            "operation": "DIFFERENTIAL",
            "arguments": [
                {
                    "operation": "POWER",
                    "arguments": [
                        {
                            "operation": "BUILD_VARIABLE",
                            "arguments": "x"
                        },
                        {
                            "operation": "BUILD_INT",
                            "arguments": "2"
                        }
                    ]
                },
                [
                    {
                        "operation": "BUILD_VARIABLE",
                        "arguments": "x"
                    }
                ]
            ]
        },
        {
            "operation": "BUILD_TENSOR",
            "arguments": "g_{mu}_{nu}"
        }
    ]
}
```
In this case there are operations such as "BUILD_TENSOR", "BUILD_VARIABLE" and  "DIFFERENTIAL", which are not supported by our default operation configurations. You can then define your own classes, place them in a dictionary and inject them into the MathInterpreter class as a parameter, which will then call your classes to handle the "arguments". 

```
OPERATION_CLASSES = {
                        "BUILD_INT"         : Int,
                        "BUILD_FLOAT"       : Float,
                        "ADD"               : Add,
                        "MULTIPLY"          : Multiply,
                        "DIVISION"          : Divition,
                        "POWER"             : Pow,
                        "BUILD_VARIABLE"    : Variable,
                        "DIFFERENTIAL"      : Differentiate,
                        "INTEGRAL"          : Integrate,
                        "BUILD_TENSOR"      : Tensor
                    }
```

Having:

```
MathInterpreter(
                    math_op             = <Your equation dictionary>, 
                    operation_classes   = OPERATION_CLASSES
                ).evaluate()
```

Now when the `evaluate()` method us called, the `MathInterpreter` class will use your own classes, which you have defined how you want to handle, say a derivative operation in `OPERATION_CLASSES`.

BUGS:

Currenctly there are lots of bugs, and errors are not handled well. The goal will be to write tests and make sure all use cases have elegant error handling. This is a work in progress.

CREDIT:

Mathyfy is an extension of the code to a more general calculator for any math object. The package was inspired by CodePulse's YouTube tutorial on "Writing a Simple Math Interpreter". It is the author's first time writing a simple language.

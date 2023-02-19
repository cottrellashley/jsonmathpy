DESCRIPTION:

Mathyfy is a Python package that can take a string as input and convert it into a JSON math file. The package can parse and evaluate expressions using the operations and objects injected by the user.

CURRENT FEATURES:

Mathyfy: A method to parse a string and return a Python dictionary representing the equation.
Evaluate: A method to evaluate the expressions based on the injected objects entered by the user that handle the operations.

FUTURE FEATURES:

Ability to execute and interpret the math JSON file by injecting a config object.
A lexer will be implemented to parse latex code.
Bugs will be fixed.

HOW TO USE:

Import Mathyfy into your Python code.
Enter an equation as a string, for example: '2+4*7'.
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
{
    "operation" : "OPERATION",
    "argument"  : [LIST of STRINGS ARGUMENT] or "STRING ARGUMENT"
}

You can store this dictionary or use the built-in evaluate method to evaluate the expression with the components you want.
To use the evaluate method, enter a dictionary with the classes that will handle the corresponding arguments. The default operation classes are:

DEFAULT_OPERATION_CLASSES = {
"BUILD_INT" : Int,
"BUILD_FLOAT" : Float,
"ADD": Add,
"MULTIPLY": Multiply,
"DIVISION": Division
}

The Multiply class is responsible for handling the "MULTIPLY" operation. These are the build in default classes. 

INJECTING YOUR OWN OPERATIONS:

You can however overide how the Evaluate class handles each of the arguments, such as:

String: 'diff(x**2, x) + g_{mu}_{nu}'

Output:

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

In this case there are operations such as "BUILD_TENSOR", "BUILD_VARIABLE" and  "DIFFERENTIAL", which are not supported by our default operation configurations. You can then define your own classes, place them in a dictionary and inject them into the MathInterpreter class as a parameter, which will then call your classes to handle the "arguments". 


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

CREDIT:

Mathyfy is an extension of the code to a more general calculator for any math object. The package was inspired by CodePulse's YouTube tutorial on "Writing a Simple Math Interpreter". It is the author's first time writing a simple language.

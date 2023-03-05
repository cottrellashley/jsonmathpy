# JsonMathPy

[JsonMathPy](https://pypi.org/project/jsonmathpy/) is a Python package that can take a string as input and parse it into a python dictionary, (and if you want a JSON math file). The package can parse and evaluate expressions using the operations and objects injected by the user.

### WHY DOES THIS EXIST?


During the creation of [RelativisticPy](https://github.com/cottrellashley/relativisticpy), I needed to be able to deserialize equations and modularize the operations (seperating the concerns) to make things simpler, more scalable and compatible with databases.


### CURRENT FEATURES:

- `Mathyfy:` Will parse a string and return a Python dictionary representing the equation.
- `MathJSONInterpreter:` Will evaluate the python dictionary based on the injected objects entered by the user that handle the operations. Or on the default operation pre-defined classes.

### USE EXAMPLES:


Install package:
```
pip install jsonmathpy
```

Import and use package:

```
import jsonmathpy as jmp
```

Use Mathyfy:

```
jmp.Mathyfy("2+4*7")()
```
Output:

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

The structure here will always be consistent with:

```
{
    "operation" : "OPERATION",
    "argument"  : [LIST of JSON MATH OBJECTS]
}

OR 

{
    "operation" : "OPERATION",
    "argument"  : "STRING ARGUMENT"
}
```
You can store this dictionary or use the built-in evaluate method to evaluate the expression with the components you want. To use the evaluate method, enter a dictionary with the classes that will handle the corresponding arguments. The default operation classes are:
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

```
String: Mathify('diff(x**2, x) + g_{mu}_{nu}')()
```

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

Or for instance an array like object with nested lists like:

- Arrays Implementation:

```
Input : [[1 + 2, 5 + 3], [2, 3]]
Output:
{
  "operation": "ARRAY",
  "arguments": [
    {
      "operation": "ARRAY",
      "arguments": [
        {
          "operation": "ADD",
          "arguments": [
            {
              "operation": "BUILD_INT",
              "arguments": "1"
            },
            {
              "operation": "BUILD_INT",
              "arguments": "2"
            }
          ]
        },
        {
          "operation": "ADD",
          "arguments": [
            {
              "operation": "BUILD_INT",
              "arguments": "5"
            },
            {
              "operation": "BUILD_INT",
              "arguments": "3"
            }
          ]
        }
      ]
    },
    {
      "operation": "ARRAY",
      "arguments": [
        {
          "operation": "BUILD_INT",
          "arguments": "2"
        },
        {
          "operation": "BUILD_INT",
          "arguments": "3"
        }
      ]
    }
  ]
}


```

In this case there are operations such as "BUILD_TENSOR", "BUILD_VARIABLE" and "DIFFERENTIAL", which are not supported by our default operation configurations. You can then define your own methods, place them in a dictionary and inject them into the MathInterpreter class as a parameter, which will then call your classes to handle the "arguments".
```
custom_operations = {
                        "BUILD_INT"         : int,
                        "ARRAY"             : array,
                        "BUILD_FLOAT"       : float,
                        "ADD"               : add,
                        "MULTIPLY"          : multiply,
                        "DIVISION"          : divition,
                        "POWER"             : pow,
                        "BUILD_VARIABLE"    : variable,
                        "DIFFERENTIAL"      : differentiate,
                        "INTEGRAL"          : integrate,
                        "BUILD_TENSOR"      : tensor
                    }
```

Having:

```

jmp.MathJSONInterpreter(
                    math_op             = <Your equation dictionary>, 
                    operation_classes   = custom_operations
                ).evaluate()
```

Now when the evaluate() method us called, the MathJSONInterpreter class will use your own classes, which you have defined how you want to handle, say a derivative operation in OPERATION_CLASSES.

### MAIN TO DO's:

- Unit tests.
- Error Handling (Ability to show user where and what the error is.)


### CREDIT:

Before this project I knew nothing of writing Lexers, Parsers or Interpreters. CodePulse's YouTube tutorial on "Writing a Simple Math Interpreter" was what I used to build upon.


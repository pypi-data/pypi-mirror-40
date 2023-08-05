Simple parsing of arguments/parameters supplied on the command line

Allows to create json file with details of the arguments/parameters available on the command line for any application. It then handles the  parsing of these parameters by setting the required flags which you can directly consume in your application. 

Helps skip the step of having to manually parse for parameters in every application

Get started by creating an object of SimpleParameters by creating its object

params = simpleparser.SimpleParameters('path to configuration files')
options, args = params.resolve_parameters(sys.argv)

Now the command line swtiches specifed in the json file are available in the options list and the positional parameters are available as args. It also generates a help file to describe the parameters available for your application. Try using -h option

There are some new features in the Projects tab TODO's if anyone is interested in picking these up.


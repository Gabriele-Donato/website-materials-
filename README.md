**The project has been updated! Here the changes: 1) I have switched from Jupyter to Pycharm; 2) I have introduced a Kafka producer that scrapes everyday the updates (stream); 3) I have momentarily suppressed the TextParser class that had been introduced in the previous version. A new function that checks whether there have been updates should be included (however this may be done once the storing system will be implemented.)**

# What is cooking?

This project is my first structured and thought attempt at using Big-Data technologie. The idea originally came from the ambition to learn and use in the same project both Hadoop and Spark. I think that the scraper (synchronous since parallelized by Spark) should send the data to Kafka, then they will have to be processed through PySpark and finally stored in a Hive table.

This is an ongoing project, so I have only rough ideas about the results, and I am motivated solely by the fact that I would like to learn these beautiful tools of big-data managemenet. Check also my [website](https://gabriele-donato.github.io/gabrieledonato/jekyll/update/2024/07/22/Updates.html) to know more.

# The state of affairs

Currently I have prepared the code so that it will be possible to focus on the data storing part and processing. In the notebook I discuss certain ideas that I deem useful but that will be applied only after I will have achieved the objective of using either/both Hadoop or/and Spark. Note that currently I do not have multiple machines, so I will work locally. My interest is understanding the components of the tools and how they interact with Python.

# Here is my horizion 

After the above general attempts I hope to achieve a generalisation of the basic code that I am currently building. Specifically:

1) A program able to retrieve data from a number of _different_ selected sources.
2) An intelligent system that is capable of understanding what are the components of the page (currently it is defined manually on homogeneous resources).
3) A number of derived datasets to be analysed through different tools.

Note that 2) has been an interest of mine since I learned webscraping, so I plan to define it in the most general way so that it can be a reusable component: finally I have the skills to tackle the problem!!



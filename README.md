**The project has been updated! Here the changes: 1) I have switched from Jupyter to Pycharm; 2) I have introduced a Kafka producer that scrapes everyday the updates (stream); 3) I have momentarily suppressed the TextParser class that had been introduced in the previous version. A new function that checks whether there have been updates should be included (however this may be done once the storing system will be implemented.)**

# What is cooking?

This project is my first structured and thought attempt at using Big-Data technologies (albeit without BigData). The idea originally came from the ambition to learn, and use in the same project, both Hadoop and Spark. The flow that I plan to realise is this: a scraper sends the data to a Kafka, then Kafka sends to Pyspark for processing, and finally everything gets stored through Hadoop (pland may change as I proceed.)

This is an ongoing project, so I have only rough ideas about the results, and I am motivated solely by the fact that I would like to learn certain beautiful tools of big-data managemenet. Check also my [website](https://gabriele-donato.github.io/gabrieledonato/jekyll/update/2024/07/22/Updates.html) to know more.

# Here is my horizion 

After the above general attempts I hope to achieve a generalisation of the basic code that I am currently building. Specifically:

1) A program able to retrieve data from a number of _different_ selected sources.
2) An intelligent system that is capable of understanding what are the components of the page (currently it is defined manually on homogeneous resources).
3) A number of derived datasets to be analysed through different tools.

Note that 2) has been an interest of mine since I learned webscraping, so I plan to define it in the most general way and make it a reusable component: finally I have the skills to conceptualise the problem!!

# What is cooking?

This project is my first structured attempt at using BigData technologies (albeit without BigData). The idea originally came from the ambition to learn, and use in the same project, both Hadoop and Spark. The flow that I planned to realise is this: a scraper sends the data to Kafka, then Kafka sends to Pyspark for processing, and finally everything gets stored through Hadoop (plans are changing though, because it turned out that Apache Kafka & Quixstreams are super cool tools, and I want to put my hands in stream processing. Nonetheless, in one way or another I would like to incorporate as many components as I can: it's just for learning.)

# Here is my horizion 

After the above general attempts I hope to achieve a generalisation of the basic code that I am currently building. Specifically:

1) A program able to retrieve data from a number of _different_ selected sources.
2) An intelligent system that is capable of understanding what are the components of the page (currently it is defined manually on homogeneous resources).
3) A number of derived datasets to be analysed through different tools.

Note that 2) has been an interest of mine since I learned webscraping, so I plan to define it in the most general way and make it a reusable component: finally I have the skills to conceptualise the problem!!

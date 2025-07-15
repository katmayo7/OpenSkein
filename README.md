# OpenSkein

A tool for fiber artists to track their yarn, projects, and patterns. It has been designed primarily with crocheting in mind and thus crocheters and knitters may find this tool most useful, however other fiber artists may still find it useful as there are many aspects that do not rely on the specific art.

Open Skein keeps databases of the following information, which may be useful to artists in the long-term: 

* Yarn encountered
* Current yarn stash
* Completed projects
* Pattern information

This allows artists to search past work for details that maybe useful moving forward. For example, an artist can check what yarn was used in a previous project, find the website link for an old pattern, or check washing instructions for a given yarn.

### Implementation Details ###

#### Yarn Database ####

The Yarn database contains all the yarn every logged, identified by brand and yarn line (e.g., Lion Brand 24/7 Cotton), and color (e.g., red, blue). It also stores important information regarding the skein such as the amount per skein, washing instructions, and yarn weight. It also stores personal notes such as their personal preference or distate for the yarn, suitable projects, etc.

#### Stash Database ####

The Stash database contains all yarn the artist currently has on hand. Yarn is identified similarly to the Yarn database, which allows for matching across the two. For example, to determine if any of the yarn in your current stash is machine washable. The Stash database allows the artist to log the amount of yarn on hand in a number of ways, allowing for maximum convience. The program will then internally calculate the remaining measurements based on the skein information logged in the Yarn database. For example, if you log the weight of the yarn remaining after finishing a project, the program will be able to calcuate the number of skeins and length (in yards and meters) of the remaining yarn being stashed.

#### Patterns Database ####

The Patterns database stores information about patterns. In particular, names, requirements (e.g., yarn weight, hook size), and where these patterns can be found. This makes it easy for artists to be able to go back and locate a pattern they previously used. It can also hold notes regarding the pattern.

#### Projects Database ####

The Projects database stores information regarding completed projects. This includes the project title, pattern and yarn information, and any personal notes the artist wishes to include. Note that the project name is a different entry from the pattern name, to allow for reference to creating a pattern multiple times. The projects database uses information from the Patterns and Yarn databases in logging information. For example, it will connect a project to its pattern listed in the Pattern database and use information in the Yarn database to log information such as the project's machine washability.

#### General Notes ####

While this tool was created mostly with crocheters in mind, it is suitable for other fiber artists as well. For example, when using the Patterns databases, a knitter may list the suggested needle size even though the database refers to the suggested hook size.

The Yarn and Pattern databases may also hold yarn and patterns not yet utilized if the artist wishes. In this way, the databases expand beyond simply logging information previously encountered, but also may store information that could be useful in to save for the future. For example, if you hear of a yarn you'd like to try in the future, you might wish to log it in the Yarn database so you don't forget. The Project database could be used similarly, though note that it will automatically store the current date as the project completion date. Therefore, if you choose to log projects you are currently or wish to complete in the future, you will loose this functionality of the database (looking at project completion dates logged will not longer provide useful information to the user).

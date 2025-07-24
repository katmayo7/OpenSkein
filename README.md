# OpenSkein

A tool for fiber artists to track their yarn, projects, and patterns. It has been designed primarily with crocheting in mind and thus crocheters and knitters may find this tool most useful, however other fiber artists may still find it useful as there are many aspects that do not rely on the specific art.

Open Skein keeps databases of the following information, which may be useful to artists in the long-term: 

* Yarn encountered
* Current yarn stash
* Completed projects
* Pattern information

This allows artists to search past work for details that maybe useful moving forward. For example, an artist can check what yarn was used in a previous project, find the website link for an old pattern, or check washing instructions for a given yarn.

### How to Use ###

Run main.py to run the command line interface for interacting with the databases.

The code will prompt you to choose what action you want to take:

* view: view one of the databases
* add: add to the database
* filter: filter a database by column values
* remove: remove from a database

It will then prompt you to input which of the databases you wish to perform this operation on: yarn, stash, project, or pattern.

The code will walk you through the details necessary to perform each operation on the desired database. See below for more info on each action.

#### View ####

View allows you to see all the entries in a specified database. You can also select a subset of columns to view. For example, you might want to look at the total amount of yarn in yards you have for all the yarn in your Stash database.

#### Add ####

Add allows you to add a new entry to a database. It will prompt you to input all necessary information and ensure you are happy with your info before adding it. It is important to note that you may get extra prompts when adding to the Stash or Project databases. The Stash database rquires that all logged yarns are also present in the Yarn database. If you add one that violates this, it will prompt you to input the necessary information to add it to the Yarn database as well and perform that add operation. Similarly, adding to the Project database requires the pattern is logged in the Pattern database and the yarns listed for the project are logged in the Yarn database. Please note, adding to the Project database will not automatically remove that yarn from your Stash, so you must do that yourself if the project affects you current stash.

#### Filter ####

Filtering allows you to show all entries that match a certain criteria specified by a column value. Depending on the column it allows you to find entries with a perfect match (e.g., yarn weight), a partial match (e.g., information in the notes), or comparatively larger/smaller than a value (e.g., total amount of yarn). Note once you've filtered your data, you can opt to view a subset of the columns for the matching entries. The code also allows you to filter a database which is the combination of the Yarn and Stash databases. This is useful for example if you want to answer queries like "What yarn in my current stash is machine washable".

#### Remove ####

You can remove an entry from either the Stash database or the Project database. You remove from the Stash by brand name and color and from the Project by project name. The Stash database allows removals because you may have finished using up all of a type of yarn. However, we want to keep a record that you once used/encountered that yarn for future reference and so we do not allow removals from the Yarn database. Removing from the Project database is allowed to provide maximium flexibility to artists for how they wish to make use of this table. The intended purpose is to log projects that are completed and so removing is not necessary. However, some may wish to use it to log all projects that have been decided (including to-be-completed) projects. And in this case, an artist may want to remove previously logged projects to represent a project being scrapped, etc.

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

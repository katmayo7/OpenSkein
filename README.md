# OpenSkein

A tool for fiber artists to track their yarn usage and projects. 

It allows artists to keep track of yarn they currently use and have used previously, which is useful for storing information about the yarn long-term. For example, washing instructions and personal thoughts which can be referenced later as needed. This allows for a searchable database of yarn tailored to the individual.

Yarn is also connected seemlessly to current and past projects making it easy to know what yarn was used on which projects.

### Implementation Details ###

The Yarn table contains all yarn ever logged. It stores important information about the yarn including skein information (amount in a skein), weight, and personal notes. This allows one to recall certain yarn that was used in the past or know which yarns to avoid. The brand name should include the company as well as the specific yarn line (ex: Malabrigo Rios).

The Stash table shows the yarn an artist currently has on hand. It lists the amount currently on hand and is connected to the Yarn table to display general information about that type of yarn. The Stash is searchable which allows an artist to see if they have any yarn matching the needs of a current project on hand. It also allows the artist to log the amount of yarn they have in a variety of ways (weight, length, number of skeins) and auto fills in the remaining details.

The Projects table stores the name of projects and can be used to track projects completed, under way, and to be started, depending on the artist's needs. The projects allow for storing of links to patterns and logs the yarn used for each project, which allows it to be connected to the Yarn table when desired. For example, if you need to recall if a certain project you made is machine washable.

The length of yarn is stored using both imperical (yards) and metric (meters) information. At the time of logging yarn, it will ask for both measurements if possible, or if not will calculate one from the other (yards from meters, etc.). This information is used to allow the Stash table to update amounts based solely on input of one measurement for ease of use.

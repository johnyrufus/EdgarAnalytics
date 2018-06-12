# Table of Contents
1. [Challenge summary](README.md#challenge-summary)
2. [Overview of the Solution](README.md#overview-of-the-solution)


# Challenge summary

For this challenge, we're asking you to take existing publicly available EDGAR weblogs and assume that each line represents a single web request for an EDGAR document that would be streamed into your program in real time. 

Using the data, identify when a user visits, calculate the duration of and number of documents requested during that visit, and then write the output to a file.

Your role on the project is to work on the data pipeline to hand off the information to the front-end. As the backend data engineer, you do **not** need to display the data or work on the dashboard but you do need to provide the information.

You can assume there is another process that takes what is written to the output file and sends it to the front-end. If we were building this pipeline in real life, we’d probably have another mechanism to send the output to the GUI rather than writing to a file. However, for the purposes of grading this challenge, we just want you to write the output to files.

# Overview of the Solution


## Design and Implementation

### LRUQueue:
We use a custom implementation of LRUQueue that uses a doubly linked list of Sessions.
A Session object represents an active ongoing session state.

The LRUQueue is the most efficient as it takes O(1) in moving the recently updated items to the front and
the expired sessions are checked from the back of the queue, until there are no more expired sessions, which is constant
time in the number of expired sessions

### LogProcessor:
The main LogProcessor class,  processes the log data as a stream and handles the LRUQueue and the set of active sessions.

Also we batch updates for a single second. To efficiently process multiple updates occuring within a single second,
we cache all the updates for a single second, squash multiple updates for a particular IP into a single update and batch process the entire data for a particular second in one shot.
This approach is efficient in reducing the number of calls to update the internal data structures.

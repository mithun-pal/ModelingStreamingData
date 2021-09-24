## Streaming Data in General:
Streaming data is continuous and urgent.
If it is not urgent, we can process it in nightly batches or whenever we felt like.
If it was not continuous then we had a clear starting and stopping point.
For low priority work we have batch Job, for small intermittent activity, we have events and transactions.But when we look at the middle we have streaming data.It's coming in fast,frequently and we need to deal with it now.

## Key consideration while modeling Streaming Data:
**What attributes or qualities do we have to think about when modeling streaming data?**  
We have to think about below characteristics for streaming data which is continuous and urgent.  
__So what does it mean for data to be continuous?__
1. __Unbounded__ - There is no concept of done, no stopping point.
2. **Difficult to model** - As there is no good starting and stopping point continuous streaming data is difficult to model.
3. __Time-based__ - Windows of time or bucket of time.Primary way to relate streaming data by timestamp.When did the event happen, when was the data created, when did we get it, and when does it become stale or out of date.

Continuous data is often about pattern in time.  
**So what does it mean for data to be urgent?**
1. **Fault-tolerant** - If there is a failure, it needs to recover from that failure quickly and efficiently. Data latency also needs to be handled.
2. __Time-sensitive__ - Urgent data decays in value over time, and if data is late to arrive because of network glitches sometime you have to
throw it out.Watermarking is the technique to decide which data to keep and which to throw out.
3. **Valuable** - Urgency implied that something bad might happen if we lose the data or can't respond to it in time. urgent data often leaves
the urgent action depending on the circumstances.This real time data helps to catch urgent issues.

Urgent means velocity of data has to be as fast as possible.  
But its not just pure speed, its speed in three places.  
We need speed at the
1. __input step__ or __ingestion step__ - Bringing the data into the System for it to be consumed and processed.
2. **processing step** - Selecting data, aggregating data, dealing with late data.
3. __output__ - Saving the results to some sort of file store or database system.
So we need high velocity going in, through and out.

## Key challenges with Streaming Data Modeling:
The inherent problem with streaming data rather modeling streaming data is not that it needs to be fast or that is big in volume in size.
But that the data changes while you're working on it.Streaming data changes midstream.  

Its changes in two specific ways.
- First its new data. This is unsurprising because the whole of Streaming data is that the new data is coming in all the time and constantly.  
So while the original data is being processed, new data is likely to come in that would change the result.
- We also have late data.This is data that arrives out of order and often quite late.This is a bigger challenge because we may have made a calculation,and then this comes in and invalidate those results.

## Solutions in Spark Streaming:
Solution to this new data and late data problems in Spark is,
- The first way Spark Structured Streaming solves this issue is working in micro batches.  
This basically means doing the work in tiny increments or batches so it doesn't have to wait for all the data to arrive to start work.  
But how do we manage the time between micro batches without rereading all of the data.  
Spark keeps track of something called **intermediate
state**.This is just enough information so that it can recalculate the final result as needed.

- Secondly Spark handles late data arrival using a technique called __watermarking__.<br>
Which is basically marking the data with a time of arrival and rejecting data that is too stale.This allows us to get rid of intermediate state after a certain point.  
once we've passed that event horizon in terms of time and staleness, we can get rid of any intermediate state data from before that, because we no longer need it.

## Handling Failure:
**How do we handle failure?**   
One of the most important part of Spark Structured Streaming is read once guarantee.It's the idea that all of the data will be processed exactly once.Not twice not zero times.And so the results are always accurate and correct.

__If a job fails midway, how do we avoid reprocessing the same data or avoid skipping important data?__  
- First is **checkpointing**.By doing micro batches we can save our progress at each checkpoint after each micro batch.But in addition to saving the batch result and where we are in the data stream,how far along we have gotten through that streaming data; we have to save this intermediate state and throw away the rest.This allows us to update our results as new and late data comes in.

- Finally we need to be able to reread and replay data in the data stream as well as update our result to the data sink.In order to truly guarantee that each bit of data is only processed once, we have to be able to restart a micro batch in case of failure.Rereading a data
source is essential to make sure that each bit of data is processed once and only once.

__Speed__, **change** and __consistency__, these three reasons why streaming data is so difficult to work with.

## Batch processing:

You have all the data, its not changing, its not moving.Nothing is arriving late.And what that means is you can process the data in a way that might not produce any results until the very end.and that's perfectly fine.You only have to output the data once.You don't need the
query to work in an incremental way.The result can be incomplete until the very very end of the job.  
Batch jobs are often easy to scale out horizontally because you don't need the result until the very end. These jobs are often quite slow.
you might be running them while activity is low. When we are dealing with batch data, we might use a technique called __MapReduce__.

## Lambda architecture:

This is basically combining Streaming and Batch processing into one result.Modern system combine streaming and batch data.  
It consists of batch layer, speed layer and serving layer. Serving layer acts as an intermediate layer between batch and application layer.

### Downsides of Lambda architecture:

- The more moving parts is added the more difficult it can be to create and maintain the solution.  
In the Lambda architecture there is a good chance that you're going to be using three different technologies, one for each of the different layers.  
This means three different sets of skills and three different solutions to maintain. This also means that you have to implement the same job in two different technologies, one to produce the result through the batch technology and one to produce the same or similar result through the streaming technology.  
Spark Structured Streaming avoids this issue.

## Spark Streaming in General:
In earlier version of Spark(prior to Spark 2.0), Streaming concept was implemented on top of Spark's Core Data structure, RDD. Which was called DStream. This was a very low level API and these days people are more likely to work with abstractions built on RDDs, like the DataFrame API or the Dataset API instead of working with RDDs directly.  
Spark 2.0 introduced the first version of higher level API, Structured Streaming built using DataFrame API or the Dataset API for building continuous application.

### RDD(Resilient Distributed Dataset):

Its a structure for the data that provides certain guarantees and allows the spark core Engine to make certain assumptions.  
The big benefit is a system that is fault tolerant, it's able to handle failure.It is based on certain assumptions that would not apply in many other data systems.  
- The first assumption is that RDDs are read only.  
That means instead of modifying the original RDD a new one is created, potentially in a chain of multiple transformations for production systems.If you have the original dataset and the list or lineage of transformations applied to it, you can recover the resulting data in case of a failure.
- RDDs are partitioned, which means they have a key that allows them to split up and processed in parallel so they can be distributed across multiple nodes.

### DStream(Discretized Stream):
So what is Dstream, This is the extension of core Spark API(RDD) to process the live stream of Data.  
This is streaming Dataset grouped by time and then those buckets of time are converted into RDDs.
This is internally represented as a sequence of RDDs.Prior version of Spark2, works with stream data using the same batch RDD abstraction.

#### Limitations of DStream:
Because the API is so low level, it does not provide the same consistency guarantees that Spark Structured Streaming does.
- Specifically there is no read once guarantee, although it does support checkpointing to save progress.
- Additionally it does not have support for late data. Data is processed based on the time it received not on the time it was created.  
This can also be a source of inconsistencies.
- In discretized stream grouping data by time is not quite possible.What you can do with Dstream is you can group on the time the event was received or processed.Basically when did we get it.

### Spark Structured Streaming:

- Spark Structured Streaming gives read once guarantee.As long as your data source supports replace and your data sink supports update.  
If there is a failure somewhere in the system,Spark will make sure that all the data is processed and output it exactly once.  
This allows you to avoiding double counting data or losing data, leading the more consistent and accurate results.

- Spark Structured Streaming handles late data.It allows you to easily mark a cut-off point in time for how late the data can be and will update running tallies gracefully as new data and late data comes in.

- Spark Structured Streaming allows us to group on when the event was created and we can go back and update our results as late data comes in.This grouping on time is sometimes called **windowing** and refers to marking a window of time to group by instead of being forced to depend on unique values.

- Spark Structured Streaming is SQL style.It uses Spark SQL library instead of having the work directly with a low level API.

- With Spark Structured Streaming you don't have to make a distinction in writing your batch jobs and your
streaming jobs.You can use the same language and API for both.Saving you from lots of work and making your results more consistent between both modes.

#### Output Mode:

Output mode matters if your data changes, i.e when we expect our results to change over time.If data doesn't change, then the results won't change.
Two different times that the data will change.
- First is new data, data that is always coming in all the time.
- Second is late data. This can force us to go back and make changes to earlier results if we're aggregating by windows of time.
- Another one is lack of change or static data.

Also Output Mode depends on what type of grouping we are doing.If we are not doing any grouping at all,
then something like append mode is great because it gets the data out as quickly as possible.

##### Different types of Output Mode:

1. __Append mode__ - If we are just dealing with new data, then the append mode is ideal.The append mode outputs the new data and it only makes appends and does not go back and change old results.

2. **Update mode** : In the case of late data update mode is ideal.Because it allows us to go back and update our results as long as we have the type of data sink that allows for changes.

3. __Complete mode__: If our data doesn't change, if we're doing batch processing or if we just don't want to think about it so much, then complete mode is ideal. Because every time it's triggered it outputs all of the results.  
Sorting only works in output mode as complete.

##### Which Output Mode to use:
The biggest defining factor of what output mode to use is what type of aggregation you are doing.
- If you are not doing any aggregation then you are going to do append mode because it will modify the rows and immediately output the results.  
Update mode does not make a lot of sense here because if you never group anything then there is no summary or aggregate results you could go back and change later.So functionally if you're not grouping by anything it's identical to append mode.  
Finally if you are not doing any kind of aggregates any kind of grouping complete mode is not supported.Complete mode would basically be a full copy of everything that was streamed.This is not ideal so this is not supported.  
Below Table depicts the summary view of which output mode to use when.


<table>
  <tr>
  <td style="border:none"></td>
  <td style="border:none"></td>
  <td colspan=3 style="text-align:center"><b>Group by</b></td>
  </tr>
  <tr>
    <td style="border:none"></td>
    <td style="border:none"></td>
    <td><b>None</b></td>
    <td><b>Time</></td>
    <td><b>Key</b></td>
  </tr>
  <tr>
    <td rowspan="3"><b>Output Mode</b></td>
    <td><b>append</b></td>
    <td>Yes</td>
    <td>Conditional Yes(Watermark)</td>
    <td>No</td>
  </tr>
  <tr>
    <td><b>update</b></td>
    <td>Conditional Yes</td>
    <td>Yes</td>
    <td>Yes</td>
  </tr>
  <tr>
    <td><b>complete</b></td>
    <td>No</td>
    <td>Yes</td>
    <td>Yes</td>
  </tr>
</table>


- If you group by windows of time, it only sort of work for append mode.Specifically you have to add a watermark and it will only output the data when the watermark point has expired.let say, after the data has become 10 minutes late or 10 minutes old then we're not going to
allow it anymore.  
Append mode will wait until it's been 10 minutes.So it knows for sure that this data could never possibly change.
<br>Update mode works great in this case because if late data arrives, spark can just go and update the data sink with any modifications.  
Complete mode also works because it only has to keep the final results and small amount of intermediate state, depending on how long the watermark is.

- If you group by a regular column then append mode doesn't work at all because it can't guarantee that the results will never change.  
append mode only works when it can guarantee that it has just outputted the final and immutable version.  
Update and complete mode works fine in this case.

#### Trigger types:
Trigger causes the data to be outputted to the data sink.  
When you run a query Spark engine needs to know when to output that data.This is determined by something called trigger.
There are three types of triggers with Spark Structured Streaming.

1. **Default(immediate)**: This is the default trigger type and basically as soon as the current micro batch finishes,it starts the next one.
So there's nothing triggering the work, it just does it as soon as physically possible.

2. __Fixed interval__: So instead of doing the work as soon as possible, you can specify a specific duration for how often to trigger.This won't go off if a micro batch is currently being processed until it's finished.So there's no risk of setting a duration so short like a
second that a bunch of concurrent batches just pile up if the system's being slammed with data.

3. **One time**: This is probably best described as an on-demand trigger.The idea here is you manually initiate a processing trigger.This makes sense when you only want the job to run occasionally.  


#### Dealing with failure:

##### 1. Delayed data:
Late arrival in data can be handled by setting something known as a __watermark__,which limits how old the data can be and still be accepted.According to Merriam-Webster one of the definition for a watermark is a mark indicating the height to which water has risen.In Spark it is not measuring height of the water it's the delay of data.

One of the benefits of **watermarking** is that as time goes on we can get rid of this information that we keep around to deal with new data and late data as it arrives.So if we have a watermark of 20 minutes then we don't need to be able to deal with late data from 8 hours ago.
We can start throwing away information we no longer need.  
In order to get this benefit we have to use either append or update mode.  
Complete mode never gets rid of intermediate state information.

###### Limitations of Watermarking:
- Data removal guarantee only goes one way.They make what you might call a negative promise.They promise that they won't throw away your data before it's expired.It is actually possible to receive data that has expired and it may still get integrated into your results if it's able to do so.It's not until Spark has thrown away the intermediate state data, that it needs to update the results, that it
will stop accepting data.  
So you can potentially receive data that is older than you expected and it will get integrated in the results if
it's able to.

- The other limitation is that the timestamp column that you use for your watermark also has to be part of your grouping operation.You either have to group on the column directly or on a window of time based on that column.
watermarks are a one way semantic guarantee, i.e they guarantee that they aren't going to throw out current data, they aren't going to throw out anything that's within that watermark. But if the state information is available for the expired data, then it will still get included.

##### 2. Node failure:
Spark Structured Streaming employs a few tools to deal with a Job failure.
- __Write-ahead logging__: This is very common in a number of systems, such as file systems and specially with relational databases.  
Write-ahead logging is the key to avoid an inconsistent state if there's a crash or error.All this means is that Spark will write to disk what it's trying to do before committing the work.That way if something fails in the middle the computer can tell where it left off.If there's a failure you don't have to redo all your work. And so as work is being done Spark will create checkpoints.**Checkpoints** are way of saving state information as the work's being done.So the system will have all of the data it needs to resume that work.In order to use checkpointing, you have to specify a storage location for this state data.  
Finally Spark allows you to resume a query if there is an error.  

__So what actually gets saved to disk when you use checkpoints?__  
There are two main things.  
  * First is the progress in the stream of data.This makes sense when you think about a re playable data source like
Kafka, which allows for applications to reread or replay through that data stream. If we are going to repeat work, we need to be able to replay or repeat information.  
  - The other one is running totals.This is all of the data we've aggregated so far.But also any intermediate information to handle new and late data.So if we are calculating average for example, Spark will temporarily track the count and sum as well so it can recalculate that
average when new data comes in.

**So how do you enable checkpointing for Spark Structured Streaming?**  
We can enable checkpointing by adding a output option("checkpointlocation","hdfs/some/path") in the final query which is triggering the computation.This location should be in a reliable file system like hdfs for production use case.

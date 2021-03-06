# <V8 on Xeon/VOX>
## High-Level Technical Design
###### Version 1.1
###### 03/28/2019


## Revision History

| Revision No. | Draft/Changes       |     Date      |    Author     |
| :----------: | :-----------------: | :-----------: | :-----------: |
|     1.0      | Initial Draft       |  2019-01-22   |       -       |
|     1.1      | Schedule Run Driver |  2019-03-28   |  Zhou, Yang   |


#### See here for information about the infrastructure in place so far:
https://github.com/zhouy7x/benchmarking/blob/master/benchmarks/README.md

## Mandate

The Benchmark working group's purpose is to gain consensus for an agreed set of benchmarks that can be used to:

1. Track and evangelize performance gains made between Node releases
2. Avoid performance regressions between releases

Its responsibilities are:

1. Identify 1 or more benchmarks that reflect customer usage.  Likely need more than one to cover typical Node use cases including low-latency and high concurrency
2. Work to get community consensus on the list chosen
3. Add regular execution of chosen benchmarks to Node builds
4. Track/publicize performance between builds/releases

The path forward is to:
 * Define the important
   [use cases](https://github.com/zhouy7x/benchmarking/blob/master/docs/use_cases.md)
 * Define the key
   [runtime attributes](https://github.com/zhouy7x/benchmarking/blob/master/docs/runtime_attributes.md)
 * Find/create benchmarks that provide good coverage for the
   use cases and attributes
   ([current table](https://github.com/zhouy7x/benchmarking/blob/master/docs/use_cases.md))
   
## Logistics

### Semi-monthly Meetings

Meetings of the working group typically occur every third Tuesday as shown on the
the node.js project [calendar](https://nodejs.org/calendar).
A few days before each meeting, an [issue](https://github.com/nodejs/benchmarking/issues)
will be created with the date and time of the meeting.
The issue will provide schedule logistics as well as
an agenda, links to meeting minutes, and
information about how to join as a participant or a viewer.

## Source github project
  + https://github.com/nodejs/benchmarking

## Current Project Team Members
  + Michael Dawson (@mhdawson) Facilitaor 
  + Uttam Pawar (@uttampawar)
  + Michael Paulson (@michaelbpaulson)
  + Gareth Ellis (@gareth-ellis)
  + Kunal Pathak (@kunalspathak)
  + Jamie Davis (@davisjam)

## Emeritus Project Team Members

  + Trevor Norris (@trevnorris)
  + Ali Sheikh (@ofrobots)
  + Yosuke Furukawa (@yosuke-furukawa)
  + Yunong Xiao (@yunong)
  + Mark Leitch (@m-leitch)
  + Surya V Duggirala (@suryadu)
  + Wayne Andrews (@CurryKitten)
  + Kyle Farnung (@kfarnung)
  + Benedikt Meurer (@bmeurer)
  + Sathvik Laxminarayan (@sathvikl)

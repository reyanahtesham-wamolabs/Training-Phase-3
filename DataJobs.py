#Once a job is added it enters this list and it is removed when a job starts. It performs the job of a priority queue
totalJobs=[]

#This is the total list of all the jobs till now produced. It is used to give stats
registryJobs=[]

#This is the list of running jobs. It is used with websockets to give updates
runningJobs=[]

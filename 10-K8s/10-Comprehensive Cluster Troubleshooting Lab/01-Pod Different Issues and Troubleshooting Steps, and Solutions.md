Pod Different Issues and Troubleshooting Steps, and Solutions (CrashLoopBackOff, ImagePullBackOff, Pending)


Image pull back error , means the image use to deploy any PODs is not present in the Image replositories.

Describing pod shows POD-terminated and reason is OOMKilled. That means POD ran out of memory. This happens when we assign limit of the POD less than its requirements.

001 -> If Pod is not assigned to a Node because of Insufficient resources, then the status of POD will be in Pending state and the reason will be "FailedScheduling".

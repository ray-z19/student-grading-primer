# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
In prior implementations, when get_stats is called in app.py, a crash will occur if there are no students in the database at the time of the function call. Most importantly, average mark is determined by dividing the mark_sum by the number of students. Dividing by zero is a methematically invalid operation, so this edge case needed to be addressed. Additionally, the minimum and maximum marks also cannot be computed due to the non-existence of students.
2) How you have accounted for this in your implementation
Before any calculation or determination of data, a check is done on the students array returned by the db function, confirming the existence of students in the database. No students means no further work is required in the get_stats function and an error code is returned instead or the requested statistics.
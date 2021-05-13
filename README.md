<p>This is a crawler which follows ABC algorithm based on URLs IP Address.</p>
<p>Requirement:<br>
Python3.6, Mysql, Beautiful Soup.</p>
<p>NOTE:  All files need to be in same folder.</p>
<ul>
<li>
<p>Creating database connections:	<br>
In DSSE_config.ini you will be making changes of the database credentials and database name as well as table name.<br>
As I am using mysql , so my code is based on mysql. You can change it to your confortable database in <a href="https://github.com/GaneshSai/Crawler/blob/master/new_crawler.py">new_crawler.py</a>, as its following SQLAlchemy.<br>
The schema of the table is DSSE.zip file. You can import that in the database.</p>
</li>
<li>
<p>Change all the file names according to your system.</p>
</li>
<li>
<p>Seed urls can be defined by your own. As I have used Information Security Wiki. But this code is worked for any domain.</p>
</li>
<li>
<p>Main file to run is <a href="https://github.com/GaneshSai/Crawler/blob/master/new_crawler.py">new_crawler.py</a> and <a href="https://github.com/GaneshSai/Crawler/blob/master/Data_CSV.py">Data_CSV.py</a>.</p>
</li>
</ul>

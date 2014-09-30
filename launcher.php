<html>
 <head>
  <title>PHP Test</title>
 </head>
 <body>
 <?php
 $command = "python /path/to/python_script.py 2>&1";
$pid = popen( $command,"r");
while( !feof( $pid ) )
{
 echo fread($pid, 256);
 flush();
 ob_flush();
 usleep(100000);
}
pclose($pid);
 ?>
 </body>
</html>
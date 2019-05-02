##### Import the Master.csv

Function Mysql{


Param(
  [Parameter(
  Mandatory = $true,
  ParameterSetName = '',
  ValueFromPipeline = $true)]
  [string]$Query
  )

$MySQLAdminUserName = ''
$MySQLAdminPassword = ''
$MySQLDatabase = ''
$MySQLHost = ''
$ConnectionString = "server=" + $MySQLHost + ";port=3306;uid=" + $MySQLAdminUserName + ";pwd=" + $MySQLAdminPassword + ";database="+$MySQLDatabase + ";SslMode=none"

Try {
  [void][System.Reflection.Assembly]::LoadWithPartialName("MySql.Data")
  $Connection = New-Object MySql.Data.MySqlClient.MySqlConnection
  $Connection.ConnectionString = $ConnectionString
  $Connection.Open()

  $Command = New-Object MySql.Data.MySqlClient.MySqlCommand($Query, $Connection)
  $DataAdapter = New-Object MySql.Data.MySqlClient.MySqlDataAdapter($Command)
  $DataSet = New-Object System.Data.DataSet
  $RecordCount = $dataAdapter.Fill($dataSet, "data")
  $DataSet.Tables[0]
  }

Catch {
  Write-Host "ERROR : Unable to run query : $query `n$Error[0]"
 }

Finally {
  $Connection.Close()
  }
  }



####insert into mysql

$hostdata = import-csv -path D:\Automation\Zoning\zoning\HBA_WWW_detail.csv

foreach ($hosts in $hostdata){

$c = 0

$g = $c++

$hostname = $hosts.HostName

$FabricName = $hosts.FabricName

$Class = $hosts.Class

$Vsan = $hosts.Vsan

$wwn = $hosts.Wwn


$query = Mysql -Query  "INSERT into  (id,HostName,FabricName,Class,VSan,Wwn) VALUES('$g','$HostName','$FabricName','$Class','$Van','$Wwn')"


}


#####Comparing Master and NETWORK


#$finalquery = Mysql -Query "SELECT BARCODE,VOLRET,STATE,FLAGS from NETWORK WHERE BARCODE IN (SELECT BARCODE from MASTER)"
##### Import the Master.csv

####Analysing Master Tape list from csv file and inserting into mysql


##pulling the output from networker server , analysing and modifying fields and pushing it to db

###Schedule this powershell script weekly once 

Function Mysql{


Param(
  [Parameter(
  Mandatory = $true,
  ParameterSetName = '',
  ValueFromPipeline = $true)]
  [string]$Query
  )

$MySQLAdminUserName = 'ZYCGIbAWMficgeia'
$MySQLAdminPassword = 'jdXEAAFAlBVCuCGY'
$MySQLDatabase = 'cf_70a697ea_ec9f_4114_8c0f_9a3891851d41'
$MySQLHost = '10.106.124.194'
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




$ips =@("Lgtohop2","Lgtohop3","Lgtowebo2","Lgtowebo3","Lgtowebo4") 

$masterfile = get-content -path D:\Automation\Tape\Master.csv

foreach($master in $masterfile){

####Inserting Master array in MySql

#$query = Mysql -Query  "INSERT into MASTER (BARCODE) VALUES('$MASTER')" ###insert with date

}

foreach ($ip in $ips){


$networkercmd =  mminfo -s $ip -q "family=tape" -r "barcode,volretent,state,volflags,type,capacity" -xc':'


$software = @()

$barcode = @()

foreach($network in $networkercmd){


$_network = $network + ":"


$softwareregex = ".+?(?=:)"

$software += Select-String -InputObject $network -Pattern $softwareregex  | % {$_.Matches.value}

$r = ([regex]'.+?(?=:)').Matches($_network)

$r[1].value
#####Compare two files#>



$barcode = $r[0].value

$volumeret = $r[1].value


$volumetrim = $volumeret -replace ":"

$state = $r[2].value

$statetrim = $state -replace ":"

$flag = $r[3].value

$flagtrim = $r[3] -replace ":"

$level = $r[4].value

$leveltrim = $r[4] -replace ":"


###Get number from level trim

$dig = ([regex]'[0-9]').Matches($leveltrim)

$leveldig = "L"+$dig.value


### Concartinate barcode and type

$barcodetype = $barcode+$leveldig

$capacity = $r[5].Value

$capacitytrim =  $r[5] -replace ":"





####insert into mysql

#$query = Mysql -Query  "INSERT into NETWORK1 (BARCODE,VOLRET,STATE,FLAGS,CAPACITY,IP) VALUES('$barcode','$volumetrim','$statetrim','$flagtrim','$capacitytrim','$ip')"



}

}


#####Comparing Master and NETWORK


#$finalquery = Mysql -Query "SELECT BARCODE,VOLRET,STATE,FLAGS from NETWORK WHERE BARCODE IN (SELECT BARCODE from MASTER)"
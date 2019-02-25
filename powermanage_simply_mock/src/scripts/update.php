<?php
#####################################################################################################
#update.php v0.1 #
#Recibe llamadas periódicas GET de HTTP enviadas por modulo Powerlink de la alarma PowerMax Pro #
#Receive periodic calls through GET command of HTTP sent from PowerLink module of PowerMax Pro panel#
#autor/author: junav (junav2@hotmail.com) #
#Fecha/Date: 08/04/2016 #
#####################################################################################################
$header = "Content-Type:text/plain; charset=UTF-8";
header($header);
print ("status=0&ka_time=50&allow=0&\n");
?>
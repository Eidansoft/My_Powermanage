<?php
########################################################################################################
#notify.php v0.1 #
#Recibe las notificaciones XML sobre HTTP enviadas por modulo Powerlink de la alarma PowerMax Pro #
#Receive XML notifications over HTTP sent from PowerLink module of PowerMax Pro panel #
#autor/author: junav (junav2@hotmail.com) #
#Fecha/Date: 06/04/2016 #
########################################################################################################
#############################################
#obtiene documento xml enviado via post #
#############################################
$xmlinput = new DOMDocument();
$xmlinput->loadXML(file_get_contents("php://input"));
$elementos = simplexml_load_string($xmlinput->saveXML());
$mensajeXML=$xmlinput->saveXML();

####################################################
#crea la respuesta HTTP #
####################################################
# se obtiene el valor del tag "index" y se devuelve en la respuesta como un data stream XML
$index=$elementos->index;
$xml = new DOMDocument();
$Element = $xml->createElement("index",$index);
$xml->appendChild($Element);
$header = "Content-Type:text/xml";
header($header);
print $xml->saveXML();
?>
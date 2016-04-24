from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
from yowsup.layers                             import YowParallelLayer
from yowsup.layers.auth                        import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.stacks import YowStack
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS
from yowsup.layers.axolotl                     import YowAxolotlLayer
from yowsup.env import YowsupEnv
import requests

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #send receipt otherwise we keep receiving the same message over and over

        if True:
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())
            self.toLower(receipt)
            r = requests.post('http://localhost/anc_mess1/', data = {'reg_token':messageProtocolEntity.getBody(),'jid':messageProtocolEntity.getFrom()})
            # outgoingMessageProtocolEntity = TextMessageProtocolEntity(
            #     messageProtocolEntity.getBody(),
            #     to = messageProtocolEntity.getFrom())
            print messageProtocolEntity.getBody()
            print str(messageProtocolEntity.getBody())
            
            
            # self.toLower(outgoingMessageProtocolEntity)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)


CREDENTIALS = ("919925195998", "xreBJQf/pitX4UW/vehe5E1IfjU=")

if __name__==  "__main__":
    layers = (
        EchoLayer,
        YowParallelLayer([YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer,
                          YowAckProtocolLayer]), YowAxolotlLayer
    ) + YOWSUP_CORE_LAYERS

    stack = YowStack(layers)
    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS)         			#setting credentials
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])   					 #whatsapp server address
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)              
    stack.setProp(YowCoderLayer.PROP_RESOURCE, YowsupEnv.getCurrent().getResource())          #info about us as WhatsApp client

    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))   					#sending the connect signal
    stack.loop() #this is the program mainloop



# List of (jid, message) tuples
	# PROP_MESSAGES = "org.openwhatsapp.yowsup.prop.sendclient.queue"
	
	# @ProtocolEntityCallback("success")
	# def sendkar(self,successProtocolEntity):
	# 	for target in self.getProp(self.__class__.PROP_MESSAGES, []):
	# 		phone, message = target
	# 		print "target: "
	# 		print target

	# 		if '@' in phone:
	# 			messageEntity = TextMessageProtocolEntity(message, to = phone)
	# 		else:
	# 			messageEntity = TextMessageProtocolEntity(message, to = "%s@s.whatsapp.net" % phone)
	# 		# self.ackQueue.append(messageEntity.getId())
	# 		print messageEntity
	# 		self.toLower(messageEntity)
# CREDENTIALS = ("919925195998", "xreBJQf/pitX4UW/vehe5E1IfjU=")
# import commands
# print commands.getstatusoutput(cmd)

# cmd = 'sudo yowsup-cli demos -c /home/gadgetman/Code/yowsup/config -s 919603427665 "Your order for token: 1 is ready."'

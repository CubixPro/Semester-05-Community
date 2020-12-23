import multiprocessing
import random
import time
import threading
import sys
import const

class Channel:
    def __init__(self, name, senderToChannel, channelToReceiver, waitTillReceived, nextTimeSlot):
        self.name               = name
        self.senderToChannel    = senderToChannel
        self.channelToReceiver  = channelToReceiver
        self.channelData        = [0 for i in range(const.totalSenderNumber)]  # channel data to be distributed
        self.waitTillReceived   = waitTillReceived #event
        self.nextTimeSlot       = nextTimeSlot # event
        self.syncValue          = 0
        


    def takeDataFromSenderAndDistribute(self):
        while True:
            # clear the receiver msg of receiving msg
            self.waitTillReceived.clear()
            self.nextTimeSlot.clear()

            for i in range(const.totalSenderNumber):
            
                data = []
                #print("waiting for data...")
                data = self.senderToChannel.recv()
                
                # update channel Data
                for i in range(len(data)):
                    self.channelData[i] += data[i] 
                
                self.syncValue += 1

                if self.syncValue == const.totalSenderNumber:   
                    # distribute over every receiver
                    for receiver in range(const.totalReceiverNumber):
                        self.channelToReceiver[receiver].send(self.channelData)

                    self.waitTillReceived.wait()
                    # print("Wait over from channel! Receiver received")
                    
                    # reset self.value and channelData for next bit transfer
                    self.syncValue = 0
                    self.channelData = [0 for i in range(len(data))]

                #self.lock.release()
                #print("LOCK RELEASED!")
                #wait untill receiver received msg
                # time.sleep(0.1)
                self.nextTimeSlot.set()
                # print("Channel Timeslot set:")
            
            self.nextTimeSlot.set()
            time.sleep(0.05)
            # print("Channel Timeslot set:")
            
    

    def startChannel(self):
        t = threading.Thread(name="channel", target=self.takeDataFromSenderAndDistribute)
        t.start()
        t.join()



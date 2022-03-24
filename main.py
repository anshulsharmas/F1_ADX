from xml.etree.ElementTree import tostring
from f1_telemetry.server import get_telemetry
from kusto.ingest import ingest_kusto
import time


batch_freq_high = 9 # 20 cars per packet * batch_freq_high(x) packets
batch_freq_low = 2

ingest_cartelemetrydataCnt = 0
ingest_cartelemetryBuffer = ""
ingest_sessiondataCnt = 0
ingest_sessiondataBuffer = ""
ingest_lapdataCnt = 0
ingest_lapdataBuffer =""
ingest_carstatusdataCnt =0
ingest_carstatusdataBuffer=""

def ingest_cartelemetrydata(packet, m_header):
    #print ("car telemetry length..", len(packet.m_carTelemetryData))
    global ingest_cartelemetryBuffer
    global ingest_cartelemetrydataCnt
    #print ("SUID ",  m_header.m_sessionUID)
    for idx,cartelemetrydata in enumerate(packet.m_carTelemetryData):
        data = [
                            m_header.m_sessionUID,
                            m_header.m_frameIdentifier,
                            m_header.m_sessionTime,
                            m_header.m_playerCarIndex,
                            idx, 
                            cartelemetrydata.m_speed,
                            cartelemetrydata.m_throttle,
                            cartelemetrydata.m_steer,
                            cartelemetrydata.m_brake,
                            cartelemetrydata.m_clutch,
                            cartelemetrydata.m_gear,
                            cartelemetrydata.m_engineRPM,
                            cartelemetrydata.m_drs,
                            cartelemetrydata.m_revLightsPercent,
                            '', #cartelemetrydata.m_brakesTemperature  fix parse issue
                            cartelemetrydata.m_tyresSurfaceTemperature[0],
                            cartelemetrydata.m_tyresSurfaceTemperature[1],
                            cartelemetrydata.m_tyresSurfaceTemperature[2],
                            cartelemetrydata.m_tyresSurfaceTemperature[3],
                            cartelemetrydata.m_tyresInnerTemperature[0],
                            cartelemetrydata.m_tyresInnerTemperature[1],
                            cartelemetrydata.m_tyresInnerTemperature[2],
                            cartelemetrydata.m_tyresInnerTemperature[3],
                            cartelemetrydata.m_engineTemperature,
                            cartelemetrydata.m_tyresPressure[0],
                            cartelemetrydata.m_tyresPressure[1],
                            cartelemetrydata.m_tyresPressure[2],
                            cartelemetrydata.m_tyresPressure[3],
                            cartelemetrydata.m_surfaceType[0],
                            cartelemetrydata.m_surfaceType[1],
                            cartelemetrydata.m_surfaceType[2],
                            cartelemetrydata.m_surfaceType[3]
                    ]
        ingest_cartelemetryBuffer += ','.join(map(str, data)) 
        ingest_cartelemetryBuffer +="\n"


    if ingest_cartelemetrydataCnt == batch_freq_high:
        #print(ingest_cartelemetryBuffer)
        ingest_kusto("CarTelemetry", ingest_cartelemetryBuffer )
        ingest_cartelemetryBuffer=""
        ingest_cartelemetrydataCnt=0
    else: 
        ingest_cartelemetrydataCnt+=1


def ingest_sessiondata(sessiondatapacket, m_header):
    global ingest_sessiondataBuffer
    global ingest_sessiondataCnt
    data =[  
            m_header.m_sessionUID,
            m_header.m_frameIdentifier,
            m_header.m_sessionTime,
            m_header.m_playerCarIndex,
            sessiondatapacket.m_weather,
            sessiondatapacket.m_trackTemperature,
            sessiondatapacket.m_airTemperature,
            sessiondatapacket.m_totalLaps,
            sessiondatapacket.m_trackId,
            sessiondatapacket.m_trackLength,
            sessiondatapacket.m_sessionType,
            sessiondatapacket.m_sessionDuration,
            sessiondatapacket.m_sessionTimeLeft
    ]
    ingest_sessiondataBuffer = ','.join(map(str, data)) 
    ingest_sessiondataBuffer +="\n"

    if ingest_sessiondataCnt == batch_freq_low:
        ingest_kusto("Session", ingest_sessiondataBuffer )
       # print(ingest_sessiondataBuffer)
        ingest_sessiondataBuffer=""
        ingest_sessiondataCnt=0
    else: 
        ingest_sessiondataCnt+=1

def ingest_participantdata(packet, m_header):
    participantdataBuffer=""
    for idx, participantdata in enumerate(packet.m_participants):
        data =[
                m_header.m_sessionUID,
                m_header.m_frameIdentifier,
                m_header.m_sessionTime,
                m_header.m_playerCarIndex,
                idx,
                packet.m_numActiveCars,
                participantdata.m_aiControlled,
                participantdata.m_driverId,
                participantdata.m_teamId,
                participantdata.m_raceNumber,
                participantdata.m_nationality,
                participantdata.m_name.decode()
        ]
        participantdataBuffer += ','.join(map(str, data))
        participantdataBuffer+="\n"
    #print(participantdataBuffer)
    ingest_kusto("Participant", participantdataBuffer)

def ingest_lapdata(packet, m_header):
    global ingest_lapdataBuffer
    global ingest_lapdataCnt
     
    for idx,lapdata in enumerate(packet.m_lapsData):
        data = [
                            m_header.m_sessionUID,
                            m_header.m_frameIdentifier,
                            m_header.m_sessionTime,
                            m_header.m_playerCarIndex,
                            idx, 
                            lapdata.m_lastLapTime,
                            lapdata.m_currentLapTime,
                            lapdata.m_bestLapTime,
                            lapdata.m_carPosition,
                            lapdata.m_currentLapNum,
                            lapdata.m_currentLapInvalid,
                            lapdata.m_lapDistance,
                            lapdata.m_totalDistance,
                            lapdata.m_gridPosition,
                            lapdata.m_pitStatus,
                            lapdata.m_penalties,
                            lapdata.m_driverStatus,
                            lapdata.m_resultStatus
                    ]
        ingest_lapdataBuffer += ','.join(map(str, data)) 
        ingest_lapdataBuffer +="\n"


    if ingest_lapdataCnt == batch_freq_high:
        #print(ingest_lapdataBuffer)
        ingest_kusto("Lap", ingest_lapdataBuffer )
        ingest_lapdataBuffer=""
        ingest_lapdataCnt=0
    else: 
        ingest_lapdataCnt+=1

def ingest_carstatusdata(packet, m_header):
    global ingest_carstatusdataBuffer
    global ingest_carstatusdataCnt
     
    for idx,carstatusdata in enumerate(packet.m_carStatusData):
        data = [
                            m_header.m_sessionUID,
                            m_header.m_frameIdentifier,
                            m_header.m_sessionTime,
                            m_header.m_playerCarIndex,
                            idx, 
                            carstatusdata.m_tractionControl,
                            carstatusdata.m_antiLockBrakes,
                            carstatusdata.m_fuelMix,
                            carstatusdata.m_fuelInTank,
                            carstatusdata.m_fuelCapacity,
                            carstatusdata.m_fuelRemainingLaps,
                            carstatusdata.m_maxRPM,
                            carstatusdata.m_idleRPM,
                            carstatusdata.m_maxGears,
                            carstatusdata.m_drsAllowed,
                            carstatusdata.m_tyresWear[0],
                            carstatusdata.m_tyresWear[1],
                            carstatusdata.m_tyresWear[2],
                            carstatusdata.m_tyresWear[3],
                            carstatusdata.m_actualTyreCompound,
                            carstatusdata.m_tyreVisualCompound,
                            carstatusdata.m_tyresDamage[0],
                            carstatusdata.m_tyresDamage[1],
                            carstatusdata.m_tyresDamage[2],
                            carstatusdata.m_tyresDamage[3],
                            carstatusdata.m_frontLeftWingDamage,
                            carstatusdata.m_frontRightWingDamage,
                            carstatusdata.m_rearWingDamage,
                            carstatusdata.m_engineDamage,
                            carstatusdata.m_gearBoxDamage,
                            carstatusdata.m_vehicleFiaFlags
                    ]
        ingest_carstatusdataBuffer += ','.join(map(str, data)) 
        ingest_carstatusdataBuffer +="\n"


    if ingest_carstatusdataCnt == batch_freq_high:
        #print(ingest_carstatusdataBuffer)
        ingest_kusto("CarStatus", ingest_carstatusdataBuffer )
        ingest_carstatusdataBuffer=""
        ingest_carstatusdataCnt=0
    else: 
        ingest_carstatusdataCnt+=1

        
if __name__ == '__main__':
    print("Server started on 20777")
    for packet, theader, m_header, player in get_telemetry():
        #print(theader, packet)
        if theader == 0:  #PacketMotionData
          """   print(theader, packet.m_wheelSpeed[0], packet.m_wheelSpeed[1],
                  packet.m_wheelSpeed[2], packet.m_wheelSpeed[3])
 """
        elif theader == 1: #PacketSessionData
            ingest_sessiondata(packet, m_header)

        elif theader == 2:
            ingest_lapdata(packet, m_header)

        elif theader == 3:
            print(dir(packet.m_eventStringCode))
            print(theader, "Event ID: ", packet.m_eventStringCode._type_)
        elif theader == 4:
            #print("ID: ", theader)
            ingest_participantdata(packet,m_header)
        elif theader == 5:
         """    for setupdata in packet.m_carSetups:
                print(theader, "Front Wing: ", setupdata.m_frontWing,
                      "Rear Wing: ", setupdata.m_rearWing,
                      "Differential on throttle: ", setupdata.m_onThrottle,
                      "Differential off throttle: ", setupdata.m_offThrottle,
                      "Front camber: ", setupdata.m_frontCamber,
                      "Rear camber: ", setupdata.m_rearCamber,
                      "Front toe: ", setupdata.m_frontToe,
                      "Rear toe: ", setupdata.m_rearToe,
                      "Front suspension: ", setupdata.m_frontSuspension,
                      "Rear suspension: ", setupdata.m_rearSuspension,
                      "Front bar: ", setupdata.m_frontAntiRollBar,
                      "Rear bar: ", setupdata.m_rearAntiRollBar,
                      "Front height: ", setupdata.m_frontSuspensionHeight,
                      "Rear height: ", setupdata.m_rearSuspensionHeight,
                      "Brake pressure (%): ", setupdata.m_brakePressure,
                      "Brake bias (%): ", setupdata.m_brakeBias,
                      "Front tyre (PSI): ", setupdata.m_frontTyrePressure,
                      "Rear tyre (PSI): ", setupdata.m_rearTyrePressure,
                      "Ballast: ", setupdata.m_ballast,
                      "Fuel Load: ", setupdata.m_fuelLoad)
 """
        elif theader == 6:
            ingest_cartelemetrydata(packet, m_header)
                
        elif theader == 7:
            ingest_carstatusdata(packet, m_header)
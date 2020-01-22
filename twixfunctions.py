import GSL.gslfunctions as GSL
import numpy as np

def twix2DCMOrientation(mapVBVDHdr):
    #Orientation information
    if ('sSpecPara','sVoI','sNormal','dSag') in mapVBVDHdr['MeasYaps']:
        NormaldSag = mapVBVDHdr['MeasYaps'][('sSpecPara','sVoI','sNormal','dSag')]
    else: 
        NormaldSag = 0.0
    
    if ('sSpecPara','sVoI','sNormal','dCor') in mapVBVDHdr['MeasYaps']:
        NormaldCor = mapVBVDHdr['MeasYaps'][('sSpecPara','sVoI','sNormal','dCor')]
    else :
        NormaldCor = 0.0

    if ('sSpecPara','sVoI','sNormal','dTra') in mapVBVDHdr['MeasYaps']:
        NormaldTra = mapVBVDHdr['MeasYaps'][('sSpecPara','sVoI','sNormal','dTra')]
    else:
        NormaldTra = 0.0
    
    if ('sSpecPara','sVoI','dInPlaneRot') in mapVBVDHdr['MeasYaps']: 
        inplaneRotation = mapVBVDHdr['MeasYaps'][('sSpecPara','sVoI','dInPlaneRot')]
    else:
        inplaneRotation = 0.0    

    TwixSliceNormal =np.array([NormaldSag,NormaldCor,NormaldTra],dtype = float)

    RoFoV = mapVBVDHdr['MeasYaps'][('sSpecPara','sVoI','dReadoutFOV')]
    PeFoV = mapVBVDHdr['MeasYaps'][('sSpecPara','sVoI','dPhaseFOV')]
    DEBUG = False;              

    dColVec_vector, dRowVec_vector = GSL.fGSLCalcPRS(TwixSliceNormal,inplaneRotation,DEBUG)

    imageOrientationPatient = np.stack((dRowVec_vector,dColVec_vector),axis = 1)
    sliceNormal = TwixSliceNormal

    columns = 1
    rows = 1
    slices= 1

    pixelSpacing = np.array([PeFoV, RoFoV]) #[RoFoV PeFoV];
    sliceThickness = mapVBVDHdr['MeasYaps'][('sSpecPara','sVoI','dThickness')]

    # Position info
    if ('sSpecPara','sVoI','sPosition','dSag') in mapVBVDHdr['MeasYaps']:
        PosdSag = mapVBVDHdr['MeasYaps'][('sSpecPara','sVoI','sPosition','dSag')]
    else: 
        PosdSag = 0.0
    
    if ('sSpecPara','sVoI','sPosition','dCor') in mapVBVDHdr['MeasYaps']:
        PosdCor = mapVBVDHdr['MeasYaps'][('sSpecPara','sVoI','sPosition','dCor')]
    else:
        PosdCor = 0.0

    if ('sSpecPara','sVoI','sPosition','dTra') in mapVBVDHdr['MeasYaps']:
        PosdTra = mapVBVDHdr['MeasYaps'][('sSpecPara','sVoI','sPosition','dTra')]
    else:
        PosdTra = 0.0

    basePosition =np.array([PosdSag, PosdCor, PosdTra],dtype = float)
    imagePositionPatient = basePosition

    return imageOrientationPatient,imagePositionPatient,pixelSpacing,sliceThickness
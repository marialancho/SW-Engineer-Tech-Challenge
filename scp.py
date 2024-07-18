from pydicom.dataset import FileMetaDataset
from pynetdicom import AE, events, evt, debug_logger
from pynetdicom.sop_class import (
    MRImageStorage, CTImageStorage, SecondaryCaptureImageStorage,
    AmbulatoryECGWaveformStorage, BasicTextSRStorage, BasicVoiceAudioWaveformStorage,
    BlendingSoftcopyPresentationStateStorage, CardiacElectrophysiologyWaveformStorage,
    ChestCADSRStorage, ColonCADSRStorage, ColorSoftcopyPresentationStateStorage,
    ComprehensiveSRStorage, ComputedRadiographyImageStorage, DigitalIntraOralXRayImageStorageForPresentation,
    DigitalIntraOralXRayImageStorageForProcessing, DigitalMammographyXRayImageStorageForPresentation,
    DigitalMammographyXRayImageStorageForProcessing, DigitalXRayImageStorageForPresentation,
    DigitalXRayImageStorageForProcessing, EncapsulatedPDFStorage, EnhancedCTImageStorage,
    EnhancedMRImageStorage, EnhancedSRStorage, EnhancedXAImageStorage, EnhancedXRFImageStorage,
    GeneralECGWaveformStorage, GrayscaleSoftcopyPresentationStateStorage, HemodynamicWaveformStorage,
    KeyObjectSelectionDocumentStorage, MammographyCADSRStorage, MRSpectroscopyStorage,
    MultiFrameGrayscaleByteSecondaryCaptureImageStorage, MultiFrameGrayscaleWordSecondaryCaptureImageStorage,
    MultiFrameSingleBitSecondaryCaptureImageStorage, MultiFrameTrueColorSecondaryCaptureImageStorage,
    NuclearMedicineImageStorage, OphthalmicPhotography16BitImageStorage, OphthalmicPhotography8BitImageStorage,
    OphthalmicTomographyImageStorage, PositronEmissionTomographyImageStorage, ProcedureLogStorage,
    RawDataStorage, RealWorldValueMappingStorage,
    RTBeamsTreatmentRecordStorage, RTBrachyTreatmentRecordStorage, RTDoseStorage, RTImageStorage,
    RTPlanStorage, RTStructureSetStorage, RTTreatmentSummaryRecordStorage, SpatialFiducialsStorage,
    SpatialRegistrationStorage, StereometricRelationshipStorage, TwelveLeadECGWaveformStorage,
    UltrasoundImageStorage, UltrasoundMultiFrameImageStorage, VLEndoscopicImageStorage,
    VLMicroscopicImageStorage, VLPhotographicImageStorage, VLSlideCoordinatesMicroscopicImageStorage,
    XRayAngiographicImageStorage, XRayRadiationDoseSRStorage
)

debug_logger()


class ModalityStoreSCP():
    def __init__(self, on_receive_callback) -> None:
        self.ae = AE(ae_title=b'STORESCP')
        self.scp = None
        self.on_receive_callback = on_receive_callback
        self._configure_ae()

    def _configure_ae(self) -> None:
        """Configure the Application Entity with the presentation context(s) which should be supported and start the SCP server.
        """
        handlers = [(evt.EVT_C_STORE, self.handle_store)]
        
        
        
        contexts = [
            MRImageStorage, CTImageStorage, SecondaryCaptureImageStorage,
        AmbulatoryECGWaveformStorage, BasicTextSRStorage, BasicVoiceAudioWaveformStorage,
        BlendingSoftcopyPresentationStateStorage, CardiacElectrophysiologyWaveformStorage,
        ChestCADSRStorage, ColonCADSRStorage, ColorSoftcopyPresentationStateStorage,
        ComprehensiveSRStorage, ComputedRadiographyImageStorage, DigitalIntraOralXRayImageStorageForPresentation,
        DigitalIntraOralXRayImageStorageForProcessing, DigitalMammographyXRayImageStorageForPresentation,
        DigitalMammographyXRayImageStorageForProcessing, DigitalXRayImageStorageForPresentation,
        DigitalXRayImageStorageForProcessing, EncapsulatedPDFStorage, EnhancedCTImageStorage,
        EnhancedMRImageStorage, EnhancedSRStorage, EnhancedXAImageStorage, EnhancedXRFImageStorage,
        GeneralECGWaveformStorage, GrayscaleSoftcopyPresentationStateStorage, HemodynamicWaveformStorage,
        KeyObjectSelectionDocumentStorage, MammographyCADSRStorage, MRSpectroscopyStorage,
        MultiFrameGrayscaleByteSecondaryCaptureImageStorage, MultiFrameGrayscaleWordSecondaryCaptureImageStorage,
        MultiFrameSingleBitSecondaryCaptureImageStorage, MultiFrameTrueColorSecondaryCaptureImageStorage,
        NuclearMedicineImageStorage, OphthalmicPhotography16BitImageStorage, OphthalmicPhotography8BitImageStorage,
        OphthalmicTomographyImageStorage, PositronEmissionTomographyImageStorage, ProcedureLogStorage,
        RawDataStorage, RealWorldValueMappingStorage,
        RTBeamsTreatmentRecordStorage, RTBrachyTreatmentRecordStorage, RTDoseStorage, RTImageStorage,
        RTPlanStorage, RTStructureSetStorage, RTTreatmentSummaryRecordStorage, SpatialFiducialsStorage,
        SpatialRegistrationStorage, StereometricRelationshipStorage, TwelveLeadECGWaveformStorage,
        UltrasoundImageStorage, UltrasoundMultiFrameImageStorage, VLEndoscopicImageStorage,
        VLMicroscopicImageStorage, VLPhotographicImageStorage, VLSlideCoordinatesMicroscopicImageStorage,
        XRayAngiographicImageStorage, XRayRadiationDoseSRStorage
                ]

        for context in contexts:
            self.ae.add_supported_context(context)

        self.scp = self.ae.start_server(('127.0.0.1', 6667), block=False, evt_handlers=handlers)
        print("SCP Server started")

    def handle_store(self, event: events.Event) -> int:
        """Callable handler function used to handle a C-STORE event.

        Args:
            event (Event): Representation of a C-STORE event.

        Returns:
            int: Status Code
        """
        dataset = event.dataset
        dataset.file_meta = FileMetaDataset(event.file_meta)

        # TODO: Do something with the dataset. Think about how you can transfer the dataset from this place 

        self.on_receive_callback(dataset)
        
        return 0x0000

import asyncio
import time
from pydicom import Dataset
from scp import ModalityStoreSCP
import aiohttp
import json


class SeriesCollector:
    """A Series Collector is used to build up a list of instances (a DICOM series) as they are received by the modality.
    It stores the (during collection incomplete) series, the Series (Instance) UID, the time the series was last updated
    with a new instance and the information whether the dispatch of the series was started.
    """
    def __init__(self, first_dataset: Dataset) -> None:
        """Initialization of the Series Collector with the first dataset (instance).

        Args:
            first_dataset (Dataset): The first dataset or the regarding series received from the modality.
        """
        self.series_instance_uid = first_dataset.SeriesInstanceUID
        self.series: list[Dataset] = [first_dataset]
        self.last_update_time = time.time()
        self.dispatch_started = False

    def add_instance(self, dataset: Dataset) -> bool:
        """Add an dataset to the series collected by this Series Collector if it has the correct Series UID.

        Args:
            dataset (Dataset): The dataset to add.

        Returns:
            bool: `True`, if the Series UID of the dataset to add matched and the dataset was therefore added, `False` otherwise.
        """
        if self.series_instance_uid == dataset.SeriesInstanceUID:
            self.series.append(dataset)
            self.last_update_time = time.time()
            return True

        return False


class SeriesDispatcher:
    """This code provides a template for receiving data from a modality using DICOM.
    Be sure to understand how it works, then try to collect incoming series (hint: there is no attribute indicating how
    many instances are in a series, so you have to wait for some time to find out if a new instance is transmitted).
    For simplyfication, you can assume that only one series is transmitted at a time.
    You can use the given template, but you don't have to!
    """

    def __init__(self) -> None:
        """Initialize the Series Dispatcher.
        """

        self.loop: asyncio.AbstractEventLoop
        self.modality_scp = ModalityStoreSCP(self.on_receive_callback)
        self.series_collector = None
    
    def on_receive_callback(self, dataset: Dataset) -> None:
        """Callback function to handle received datasets from the SCP.

        Args:
            dataset (Dataset): The received dataset.
        """
        if self.series_collector is None:
            self.series_collector = SeriesCollector(dataset)
        else:
            added = self.series_collector.add_instance(dataset)
            if not added:
                print(f"Received instance for unknown series {dataset.SeriesInstanceUID}")
    

    async def main(self) -> None:
        """An infinitely running method used as hook for the asyncio event loop.
        Keeps the event loop alive whether or not datasets are received from the modality and prints a message
        regulary when no datasets are received.
        """
        while True:
            # TODO: Regulary check if new datasets are received and act if they are.
            # Information about Python asyncio: https://docs.python.org/3/library/asyncio.html
            # When datasets are received you should collect and process them
            # (e.g. using `asyncio.create_task(self.run_series_collector()`)
                        
            print("Waiting for Modality")
            await asyncio.sleep(0.2)
            await self.dispatch_series_collector()
            
            
            

    async def run_series_collectors(self) -> None:
        """Runs the collection of datasets, which results in the Series Collector being filled.
        """
        # TODO: Get the data from the SCP and start dispatching
        if self.series_collector is not None and not self.series_collector.dispatch_started:
            self.series_collector.dispatch_started = True
            series_data = self.extract_series_info(self.series_collector.series)
            await self.send_series_to_server(series_data)
            self.series_collector = None  # Reset the series collector after dispatch
        
        

    async def dispatch_series_collector(self) -> None:
        """Tries to dispatch a Series Collector, i.e. to finish it's dataset collection and scheduling of further
        methods to extract the desired information.
        """
        # Check if the series collector hasn't had an update for a long enough timespan and send the series to the
        # server if it is complete
        # NOTE: This is the last given function, you should create more for extracting the information and
        # sending the data to the server
                 
                    
        maximum_wait_time = 1
        current_time = time.time()
        if self.series_collector and (current_time - self.series_collector.last_update_time) > maximum_wait_time:
            await self.run_series_collectors()


    def extract_series_info(self, series):
        """Extract information from the series of DICOM datasets.
        
            
            Args:
                series (list[Dataset]): The series of datasets.

            Returns:
                dict: The extracted information.
        """
        series_info = {
            'SeriesInstanceUID': series[0].SeriesInstanceUID,
            'PatientID': series[0].PatientID,
            'PatientName': str(series[0].PatientName),
            'StudyInstanceUID': series[0].StudyInstanceUID,
            'InstancesCount': len(series)
        }
        return series_info

    async def send_series_to_server(self, series_info):
        """Send the extracted series information to the server.

        Args:
            series_info (dict): The extracted information.
        """
        print("Sending series info:", series_info)
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post('http://localhost:8000/store', json=series_info, ssl=False) as response:
                    if response.status == 200:
                        print(f"Successfully sent series {series_info['SeriesInstanceUID']} to server")
                    else:
                        print(f"Failed to send series {series_info['SeriesInstanceUID']} to server")
            except Exception as e:
                print(f"Error sending series to server: {e}")
                
                
if __name__ == "__main__":
    """Create a Series Dispatcher object and run it's infinite `main()` method in a event loop.
    """
    engine = SeriesDispatcher()
    engine.loop = asyncio.get_event_loop()
    engine.loop.run_until_complete(engine.main())

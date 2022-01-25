from opteryx.storage import BasePartitionScheme


class MabelPartitionScheme(BasePartitionScheme):
    def __init__(self):
        """
        Handle reading data using the Mabel partition scheme.
        """
        pass

    def partition_format(self):
        return "year_{yyyy}/month_{mm}/day_{dd}"

    def filter_blobs(self, list_of_blobs):
        def _extract_as_at(path):
            parts = path.split("/")
            for part in parts:
                if part.startswith("as_at_"):
                    return part
            return ""

        # work out if there's an as_at part
        as_ats = {_extract_as_at(blob) for blob in list_of_blobs if "as_at_" in blob}
        if as_ats:
            as_ats = sorted(as_ats)
            as_at = as_ats.pop()

            is_complete = lambda blobs, as_at: any(
                [blob for blob in blobs if as_at + "/frame.complete" in blob]
            )
            is_invalid = lambda blobs, as_at: any(
                [blob for blob in blobs if (as_at + "/frame.ignore" in blob)]
            )

            while not is_complete(list_of_blobs, as_at) or is_invalid(
                list_of_blobs, as_at
            ):
                if len(as_ats) > 0:
                    as_at = as_ats.pop()
                else:
                    return []

            # get_logger().debug(f"Reading Frame `{as_at}`")
            return [blob for blob in list_of_blobs if (as_at in blob)]

        return list_of_blobs
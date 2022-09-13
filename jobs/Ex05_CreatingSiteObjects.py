# Importing Job from nautobot.extras.jobs is required for any Nautobot job.
from nautobot.extras.jobs import Job

# These imports are the type of inputs that are being used in this job.
from nautobot.extras.jobs import StringVar, ObjectVar

# Importing models allow us to work with/manipulate objects of these types
from nautobot.dcim.models import Site
from nautobot.extras.models import Status

# This import is for the error that would be generated if we try to create a
# site that already exists
from django.db.utils import IntegrityError

# This is the job grouping within the Nautobot UI.
name = "AD Example jobs"

# This is the job being imported.
class Ex05_CreatingSiteObjects(Job):
  # This will be a simple string for the site name
  site_name = StringVar(
    default = "Nautobot Examples - Example Site",
    description = "Name of the site to be created",
    label = "Site Name"
  )

  # This pulls in the statuses in Nautobot then uses query_params to filter down
  # the types of objects so that only statuses that can be applied to Site
  # objects are available
  site_status = ObjectVar(
    description = "Set the configured status of the site",
    label = "Site status",
    model = Status,
    query_params = {"content_types": "dcim.site"},
    display_field = "name"
  )

  # The Meta class within the job class is used for job extensible data
  class Meta():
    # This is what the job will be named in the UI.
    name = "Example 05 - Creating Site Objects"
    # The first line of the description will be displayed but other lines will
    #   only be displayed on job details.
    description = """
      This job will create a base site with the user inputted name.
    """

  # This will be run when the job starts.
  def run(self, data, commit):
    # Basic log
    self.log_info("Job start")

    # Store the inputs and log them
    site_name = data.get("site_name")
    site_status = data.get("site_status")
    self.log_info(f"Site name: {site_name}")
    self.log_info(f"Site status: {site_status}")

    # Create the site
    try:
      new_site = Site.objects.create(name=site_name, status=site_status)
    except IntegrityError:
      self.log_failure("Error! The site \"{site_name}\" already exists!")

    # Log the site
    self.log_success(obj=new_site, message=f"Site \"{site_name}\" created!")

"""
This dirty script uses a selenium client to check if the frontend part of the cms_forms works as intended.
"""

import django

django.setup()  # noqa

import os
import time

from cms.api import add_plugin
from django.contrib.auth import get_user_model
from selenium import webdriver

from cms_forms.importer import TypeReference
from cms_forms.plugins.fields import CharFieldPlugin, GenericIPAddressFieldPlugin
from cms_forms.plugins.forms import SavingFormPlugin
from cms_forms.plugins.buttons import SubmitButtonPlugin
from cms_forms.models import FormSubmission
from tests.utils import PluginTestCase, safe_register


# Get config
app_host = os.environ.get("APP_HOST", "localhost")
app_port = os.environ.get("APP_PORT", "8000")
hub_host = os.environ.get("HUB_HOST", "localhost")
hub_port = os.environ.get("HUB_PORT", "4444")
app_url = f"http://{app_host}:{app_port}/"


# Init CMS objects
safe_register(SavingFormPlugin)
safe_register(CharFieldPlugin)
safe_register(GenericIPAddressFieldPlugin)
user = get_user_model().objects.create_superuser("admin", "admin@admin.com", "admin")
page = PluginTestCase.create_homepage(None, title="home", template="base.html", language="en-us", created_by=user,)
placeholder = page.placeholders.all().first()
form = add_plugin(
    placeholder=placeholder,
    plugin_type=SavingFormPlugin,
    language="en-us",
    name="form1",
    form_type=TypeReference("cms_forms.forms.SavingForm"),
)
field1 = add_plugin(
    placeholder=placeholder,
    plugin_type=CharFieldPlugin,
    language="en-us",
    target=form,
    name="field1",
    field_type=TypeReference("django.forms.fields.CharField"),
    field_parameters={},
)
field2 = add_plugin(
    placeholder=placeholder,
    plugin_type=GenericIPAddressFieldPlugin,
    language="en-us",
    target=form,
    name="field2",
    field_type=TypeReference("django.forms.fields.GenericIPAddressField"),
    field_parameters={},
)
submit = add_plugin(
    placeholder=placeholder,
    plugin_type=SubmitButtonPlugin,
    language="en-us",
    target=form,
    name="submit",
    input_type="submit",
)
page.publish("en-us")


# Init driver
driver = webdriver.Remote(
    f"http://{hub_host}:{hub_port}/wd/hub", desired_capabilities=webdriver.DesiredCapabilities.CHROME
)
driver.implicitly_wait(10)
driver.set_page_load_timeout(10)
time.sleep(2)  # ensure the server started


# Open pge
driver.get(app_url)
time.sleep(1)
page_source = driver.page_source
assert driver.current_url == app_url
assert "submitCMSForm" in page_source, page_source
assert '<input type="text" name="field1"' in page_source, page_source

# Submit broken form
driver.find_element_by_name("field1").send_keys("test_data 1234")
driver.find_element_by_name("field2").send_keys("8")
driver.find_element_by_name("submit").click()
time.sleep(1)
page_source = driver.page_source
assert driver.current_url == app_url
assert FormSubmission.objects.count() == 0
assert "submitCMSForm" in page_source, page_source
assert 'value="8"' in page_source, page_source

# Submit complete form
driver.find_element_by_name("field2").send_keys(".8.8.8")
driver.find_element_by_name("submit").click()
time.sleep(1)
assert driver.current_url == app_url
submission = FormSubmission.objects.get()
assert submission.form_name == "form1", submission.form_name
assert submission.data == {"field1": "test_data 1234", "field2": "8.8.8.8"}, submission.data


# Cleanup
driver.close()
driver.quit()

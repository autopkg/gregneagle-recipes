11/28/2018

The previous BluejeansPlugin recipes have been removed.

The previous BluejeansApp.download and .pkg recipes have been removed as they only worked for the 1.x Blue Jeans App.

The BluejeansAppURLProvider has been removed.

The BluejeansApp.munki and BluejeansApp.install recipes are now children of the moofit-recipes bluejeans.download recipe, and so that recipe repo is required to use these two recipes.

5/7/2019

I'm deprecating the BluejeansApp.munki and BluejeansApp.install recipes as I don't use them any longer and they are just a burden to maintain.
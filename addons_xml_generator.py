""" addons.xml generator """

import os
import md5


class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.
    """
    def __init__( self ):
        # generate files
        self._generate_addons_file()
        self._generate_md5_file()
        # notify user
        print "Finished updating addons xml and md5 files"

    def _generate_addons_file( self ):
        # addon list
        addons = os.listdir( "." )
        # final addons text
        addons_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n"
        # loop thru and add each addons addon.xml file
        for addon in addons:
            try:
                # skip any file or .svn folder
                if ( not os.path.isdir( addon ) or addon == ".svn" or addon == ".git" or addon == ".gitattributes" or addon == ".gitignore" or addon == "README"): continue
                # create path
                _path = os.path.join( addon, "addon.xml" )
                # split lines for stripping
                xml_lines = open( _path, "r" ).read().splitlines()
                # new addon
                addon_xml = ""
                # loop thru cleaning each line
                for line in xml_lines:
                    # skip encoding format line
                    if ( line.find( "<?xml" ) >= 0 ): continue
                    # add line
                    addon_xml += unicode( line.rstrip() + "\n", "UTF-8" )
                # we succeeded so add to our final addons.xml text
                addons_xml += addon_xml.rstrip() + "\n\n"
            except Exception, e:
                # missing or poorly formatted addon.xml
                print "Excluding %s for %s" % ( _path, e, )
        
        #add repo addon
        repo_addon_xml = """
<addon id="repository.veetv_xbmc.dev" name="VeeTV XBMC Add-ons" version="0.1.1" provider-name="VeeTV.net">
    <extension point="xbmc.addon.repository" name="VeeTV XBMC Add-ons Repository">
        <info compressed="false">http://github.com/veetvdotnet/veetv_xbmc/raw/master/addons.xml</info>
        <checksum>http://github.com/veetvdotnet/veetv_xbmc/raw/master/addons.xml.md5</checksum>
        <datadir zip="true">https://github.com/veetvdotnet/veetv_xbmc/raw/master/repository/</datadir>
    </extension>
    <extension point="xbmc.addon.metadata">
        <summary>Install add-ons from VeeTV XBMC repository</summary>
        <description>Download and install XBMC add-ons by VeeTV.net</description>
        <disclaimer>For personal use only</disclaimer>
        <platform>all</platform>
    </extension>
</addon>
"""
        
        addons_xml = addons_xml + repo_addon_xml
        # clean and add closing tag
        addons_xml = addons_xml.strip() + u"\n\n\n</addons>\n"
        # save file
        self._save_file( addons_xml.encode( "UTF-8" ), file="addons.xml" )

    def _generate_md5_file( self ):
        try:
            # create a new md5 hash
            m = md5.new( open( "addons.xml" ).read() ).hexdigest()
            # save file
            self._save_file( m, file="addons.xml.md5" )
        except Exception, e:
            # oops
            print "An error occurred creating addons.xml.md5 file!\n%s" % ( e, )

    def _save_file( self, data, file ):
        try:
            # write data to the file
            open( file, "w" ).write( data )
        except Exception, e:
            # oops
            print "An error occurred saving %s file!\n%s" % ( file, e, )


if ( __name__ == "__main__" ):
    # start
    Generator()
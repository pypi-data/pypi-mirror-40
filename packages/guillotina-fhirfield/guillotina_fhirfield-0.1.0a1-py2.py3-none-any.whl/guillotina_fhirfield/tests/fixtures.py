from guillotina import testing


def base_settings_configurator(settings):

    if 'applications' not in settings:
        settings['applications'] = list()

    if 'guillotina_elasticsearch' in settings['applications']:
        settings['applications'].append('guillotina_elasticsearch')

    settings['applications'].append('guillotina_fhirfield')
    settings['applications'].append('guillotina_fhirfield.tests.fhir_contents')


testing.configure_with(base_settings_configurator)

"""
    This behavior file contains the logic for a subset of commands. Logic specific to
    commands should be implamented in corresponding behavior files.
"""

from cli import pyke
import requests
import click
import json
import os

class ExperienceBehavior:
  def __init__(self, **kwargs):
    profile = kwargs.get('profile')
    self.util = pyke.Util(profile=profile)
    if profile is not None:
      self.context = pyke.auth.load_cache()

    self.object_type = 'experience'
    self.json = kwargs.get('json', False)
    self.profile = profile
    self.namespace = kwargs.get('namespace')
    self.format = kwargs.get('format')
    self.filter = kwargs.get('filter')
    self.page = kwargs.get('page')
    self.pagesize = kwargs.get('pagesize')
    # Expand the filename and get the absolute path. Relative paths won't resolve if entered via prompt
    self.filename = os.path.abspath(os.path.expanduser(kwargs.get('filename')))
    self.collection_name = kwargs.get('collection_name')
    self.type = kwargs.get('type')
    self.redirect_url = kwargs.get('redirect_url')
    self.description = kwargs.get('description')
    self.label = kwargs.get('label')
    self.activation_code = kwargs.get('activation_code')
    self.is_template = kwargs.get('is_template', False)

    if self.type is None:
      self.type = 'template' if self.is_template else 'standard'

  def list(self):
    data = {'filter': self.filter, 'page': self.page, 'pagesize': self.pagesize}

    resp = self.util.cli_request('GET',
      self.util.build_url('{app}/iot/v1/experiences?page={page}&pagesize={pagesize}&{filter}', {**data} ))

    if self.json:
      click.echo(json.dumps(resp))
      return

    self.util.print_table(resp.get('payload', {}).get('data', {}), self.format)
    self.util.print_record_count(resp)

  def export(self):
    # Determine if we have to lookup the namespace
    if not self.namespace:
      if self.label:
        experience_resp = self.util.cli_request('GET',
          self.util.build_url('{app}/iot/v1/experiences?{filter}', {'filter': 'label={}'.format(self.label)} ))

        experience_data = experience_resp.get('payload', {}).get('data')
        if len(experience_data) == 0:
          raise click.ClickException('Experience label "{}" not found'.format(self.label))

        if len(experience_data) > 1:
          raise click.ClickException('More than one experience was found with the label "{}"'.format(self.label))

        self.namespace = experience_data[0].get('name')
      else:
        raise click.ClickException('Must provide namespace or label of the experience to export')

    export_resp = self.util.cli_request('POST', self.util.build_url('{app}/iot/v1/experiences/{name}/export', {'name': self.namespace}))
    if self.json:
      click.echo(json.dumps(export_resp))
      return

    status_id = export_resp.get('payload', {}).get('data', {}).get('statusId', {})
    status_resp = self.util.show_progress(status_id, label='Exporting experience')

    error_msg = status_resp.get('payload', {}).get('data', {}).get('errorMessage')
    if error_msg is not None:
      raise click.ClickException(click.style('Export failed. {}'.format(error_msg), fg='red'))

    click.echo(' ')

    file_url = status_resp.get('payload', {}).get('data', {}).get('summary', {}).get('fileInfo', {}).get('signedUrl')
    file_resp = requests.get(file_url)
    with open(self.filename, 'wb') as f:
      f.write(file_resp.content)

    click.echo('Saved to {}'.format(self.filename))

  def import_(self):
    if not self.json:
      click.echo('Uploading file...')

    # Request ephemeral token
    token_resp = self.util.cli_request('GET', self.util.build_url('{app}/iot/v1/files/ephemeral?contentType=application/json'))
    token_data = token_resp.get('payload', {}).get('data', {})
    token_fields = token_data.get('fields')

    aws_access_key_id = token_fields.get('AWSAccessKeyId')
    ephemeral_key = token_fields.get('key').replace('${filename}', 'import.json')
    policy = token_fields.get('policy')
    signature = token_fields.get('signature')
    url = token_data.get('url')

    # Post to ephemral URL
    data = {
      'AWSAccessKeyId': aws_access_key_id,
      'key': ephemeral_key,
      'policy': policy,
      'signature': signature,
      'Content-Type': 'application/json'
    }

    aws_resp = None
    with open(self.filename, 'rb') as f:
      files = {
        'file': f
      }

      aws_resp = requests.post(url, data=data, files=files)

    if not self.json:
      click.echo('File uploaded.')
      click.echo('')

    collection_query_data = {'filter': self.filter, 'page': self.page, 'pagesize': self.pagesize}
    collection_resp = self.util.cli_request('GET',
      self.util.build_url('{app}/iot/v1/experience-collections?{filter}', {'filter': 'name={}'.format(self.collection_name)}))

    collection_data = collection_resp.get('payload', {}).get('data')
    if len(collection_data) == 0:
      raise click.ClickException('Collection name "{}" not found'.format(self.collection_name))

    if len(collection_data) > 1:
      raise click.ClickException('More than one collection was found with the name "{}"'.format(self.collection_name))

    # Post to import
    import_json = {
      'name':'',
      'description': self.description,
      'type': self.type,
      'experienceCollectionId': collection_resp.get('payload').get('data')[0].get('id'),
      'label': self.label,
      'redirectUrl': self.redirect_url,
      'code': self.activation_code,
      'ephemeralKey': ephemeral_key
    }

    import_resp = self.util.cli_request('POST', self.util.build_url('{app}/iot/v1/experiences/import'), json=import_json)
    if self.json:
      click.echo(json.dumps(import_resp))
      return

    status_id = import_resp.get('payload', {}).get('data', {}).get('statusId', {})
    status_resp = self.util.show_progress(status_id, label='Importing experience')

    error_msg = status_resp.get('payload', {}).get('data', {}).get('errorMessage')
    if error_msg is not None:
      raise click.ClickException(click.style('Import failed. {}'.format(error_msg), fg='red'))

    click.echo('Sucessfully imported experience.')

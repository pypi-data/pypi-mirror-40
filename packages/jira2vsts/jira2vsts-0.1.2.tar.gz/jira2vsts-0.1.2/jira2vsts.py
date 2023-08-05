#!/usr/bin/env python
import logging
import logging.handlers
import os
import time
import traceback
from datetime import datetime
from urllib.parse import urljoin, urlparse

import click as click
import validictory
import yaml
from dateutil.parser import parse
from jira import JIRA
from msrest.authentication import BasicAuthentication
from vsts.build.v4_0.models import JsonPatchOperation
from vsts.vss_connection import VssConnection
from vsts.work_item_tracking.v4_1.models import Wiql

SCHEMA_GLOBAL = {
    "type": "object",
    "properties": {
        "jira": {
            "type": "object",
            "required": False,
            "properties": {
                "url": {
                    "type": "string",
                    "required": True,
                },
                "username": {
                    "type": "string",
                    "required": True,
                },
                "password": {
                    "type": "string",
                    "required": True,
                }
            },
        },
        "vsts": {
            "type": "object",
            "required": False,
            "properties": {
                "access_token": {
                    "type": "string",
                    "required": True,
                },
                "url": {
                    "type": "string",
                    "required": True,
                }

            },
        },
        "projects": {
            "required": True,
            "type": "object",
            "patternProperties": {
                ".*": {
                    "type": "object",
                    "properties": {
                        "last_sync": {
                            "type": "string",
                            "required": False,
                        },
                        "active": {
                            "type": "boolean",
                            "required": True,
                        },
                        "name": {
                            "type": "string",
                            "required": True,
                        },
                        "type": {
                            "type": "string",
                            "required": True,
                            "enum": ['task', 'issue', 'feature', 'requirement'],
                        },
                        "default_values": {
                            "required": True,
                            "type": "object",
                            "patternProperties": {
                                "System.State": {
                                    "type": "string",
                                    "required": True,
                                    "enum": ['New', 'Proposed'],
                                },
                                ".*": {
                                    "type": "string",
                                },

                            }
                        },
                        "states": {
                            "type": "array",
                            "required": True,
                        },
                    },

                },
            },
        },
        "states": {
            "required": True,
            "type": "object",
            "patternProperties": {
                ".*": {
                    "type": "string",
                },
            },
        },

    }
}


def _create_work_item_field_patch_operation(op, field, value):
    if field.startswith('/'):
        path = field
    else:
        path = '/fields/{field}'.format(field=field)
    patch_operation = JsonPatchOperation()
    patch_operation.op = op
    patch_operation.path = path
    patch_operation.value = value
    return patch_operation


def __validate_and_get_data(config, logger, validate):
    content = open(config, 'r').read()
    try:
        content = yaml.load(content)
        validictory.validate(content, SCHEMA_GLOBAL)
    except:
        if validate:
            click.secho(traceback.format_exc())
        logger.error(traceback.format_exc())
        raise click.Abort()
    logger.info('Format of the config file is valid')
    if validate:
        click.echo('Format of the config file is valid')
    return content


def __get_logger(logfile):
    logger = logging.getLogger('jira2vsts')
    logger.setLevel(logging.DEBUG)
    fh = logging.handlers.RotatingFileHandler(logfile, 'a', 100000, 10)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def __update_config_file(config, data):
    f = open(config, 'w+')
    f.write(yaml.dump(data, default_flow_style=False, allow_unicode=True))
    f.close()


def _str_to_html(text):
    return text.replace("\n", "<br />").replace("\r", "<br />")


@click.command()
@click.option('--validate', '-v', is_flag=True, default=False, type=click.BOOL)
@click.option('--logfile', '-l',
              type=click.Path(file_okay=True, dir_okay=False, writable=True, readable=True, resolve_path=True,
                              allow_dash=True), required=True, help="Path to logfile")
@click.option('--config', '-c',
              type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True, readable=True,
                              resolve_path=True, allow_dash=True), required=True, help="Path to the configuration file")
@click.option('--loop-every', type=click.INT, default=0, help="Loop every X minutes")
@click.pass_context
def cli(ctx, validate, logfile, config, loop_every):
    """CLI for Jira2Vsts"""
    logger = __get_logger(logfile)
    while True:
        try:
            _main(ctx, validate, logger, config)
        except:
            logger.error(traceback.format_exc())
        if loop_every:
            time.sleep(loop_every * 60)
        else:
            break


def _main(ctx, validate, logger, config):
    """CLI for Jira2Vsts"""
    start = time.time()
    nbr_issues = 0
    data = __validate_and_get_data(config, logger, validate)
    VSTS_URL = data['vsts']['url']
    VSTS_TOKEN = data['vsts']['access_token']
    JIRA_URL = data['jira']['url']
    PROJECTS = data['projects']
    JIRA_PROJECTS = [k for k, v in data['projects'].items() if v['active']]
    JIRA_USERNAME = data['jira']['username']
    JIRA_PASSWORD = data['jira']['password']
    STATES = data.get('states', {})
    JIRA_BROWSE = urljoin(JIRA_URL, os.path.normpath(urlparse(JIRA_URL).path) + '/browse/%s')
    NOW = datetime.now().isoformat()
    try:
        jira = JIRA(JIRA_URL, basic_auth=(JIRA_USERNAME, JIRA_PASSWORD))
        logger.info('connection successful to jira')
        if validate:
            click.echo('connection successful to jira')
    except:
        if validate:
            click.echo(traceback.format_exc())
        logger.error(traceback.format_exc())
        raise click.Abort()

    try:
        credentials = BasicAuthentication('', VSTS_TOKEN)
        connection = VssConnection(base_url=VSTS_URL, creds=credentials)
        wit_client = connection.get_client(
            'vsts.work_item_tracking.v4_1.work_item_tracking_client.WorkItemTrackingClient')
        logger.info('connection successful to vsts')
        if validate:
            click.echo('connection successful to vsts')
    except:
        if validate:
            click.echo(traceback.format_exc())
        logger.error(traceback.format_exc())
        raise click.Abort()
    if validate:
        raise click.Abort()
    # STARTING THE PROCESS
    logger.info('start processing after connecting')
    logger.info('Jira projects to process : %s', JIRA_PROJECTS)
    for jira_project in JIRA_PROJECTS:
        vsts_default_values = PROJECTS[jira_project].get('default_values', {})
        LAST_SYNC = PROJECTS[jira_project].get('last_sync')
        PROJECTS[jira_project]['last_sync'] = NOW
        PROJECT_STATES = PROJECTS[jira_project].get('states', [])
        vsts_project = PROJECTS[jira_project]['name']
        vsts_type = PROJECTS[jira_project]['type']
        logger.info('starting jira project [%s] to [%s]', jira_project, vsts_project)
        logger.info('last sync is : %s', LAST_SYNC)
        if LAST_SYNC:
            last_sync_formatted = parse(LAST_SYNC).strftime('%Y/%m/%d %H:%M')
            jira_issues = jira.search_issues('project=%s AND updated >= "%s"' % (jira_project, last_sync_formatted))
        else:
            jira_issues = jira.search_issues('project=%s' % jira_project)
        JIRA_ITEMS = {j.key for j in jira_issues}
        logger.info('jira issues to send : %s', JIRA_ITEMS)
        for jira_item in JIRA_ITEMS:
            nbr_issues += 1
            issue = jira.issue(jira_item)
            issue_title = "{} / {}".format(jira_item, issue.fields.summary)
            updated = parse(issue.fields.updated).strftime('%d/%m/%Y %H:%M')
            issue_description = """URL: <a href="{url}" target="_blank">{url}</a>
Reporter: {f.reporter}
Update: {updated}

<strong><u>ORIGINAL MESSAGE:</u></strong>
{f.description}
            """.format(i=issue, f=issue.fields, url=JIRA_BROWSE % jira_item, updated=updated)
            issue_description_comments = []
            for jira_comment in issue.fields.comment.comments:
                jira_comment = _str_to_html(
                    "<strong>Date :</strong> {dt}\n<strong>Author :</strong> {author}\n<strong>Message : </strong>{body}""".format(
                        dt=parse(jira_comment.raw['updated']).strftime('%d/%m/%Y %H:%M'),
                        author=jira_comment.raw['author']['displayName'],
                        body=jira_comment.raw['body']
                    ))
                issue_description_comments.append(jira_comment)
            if issue_description_comments:
                issue_description += """\n<strong><u>ORIGINAL COMMENTS:</u></strong>\n"""
                issue_description += "\n\n".join(issue_description_comments)
            wiql = Wiql(
                query="""
                        SELECT [System.Id]
                        FROM WorkItems
                        WHERE 
                        [System.Title] contains "%s" AND
                        [System.TeamProject] = "%s"
                        """ % (jira_item, vsts_project)
            )
            wiql_results = wit_client.query_by_wiql(wiql).work_items
            work_items = (
                wit_client.get_work_item(int(res.id)) for res in wiql_results
            )
            vsts_id = False
            for work_item in work_items:
                workitem_name = work_item.fields.get('System.Title', '')
                if workitem_name and workitem_name.startswith(jira_item):
                    vsts_id = work_item.id
            document = []
            document.append(_create_work_item_field_patch_operation('add', 'System.Title', issue_title))
            document.append(
                _create_work_item_field_patch_operation('add', 'System.Description', _str_to_html(issue_description)))
            try:
                if not vsts_id:
                    logger.info('create a new work item with state=%s for %s', STATES.get(issue.fields.status.name),
                                jira_item)

                    for default_key, default_value in vsts_default_values.items():
                        document.append(_create_work_item_field_patch_operation('add', default_key, default_value))
                    workitem = wit_client.create_work_item(project=vsts_project, type=vsts_type, document=document)
                    vsts_id = workitem.id
                    logger.info('workitem is created id=%s source=%s', vsts_id, jira_item)
                else:
                    logger.info('update work item with id=%s, state=%s for %s', vsts_id,
                                STATES.get(issue.fields.status.name),
                                jira_item)
                    workitem = wit_client.update_work_item(id=vsts_id, document=document)
                    logger.info('workitem is updated id=%s source=%s', vsts_id, jira_item)
                # Process comments and attachments
                relations = workitem.relations if workitem.relations else []
                exists_attachments = [x.attributes.get('name') for x in relations if x.rel == 'AttachedFile']
                for attachment in issue.fields.attachment:
                    attachment_filename = attachment.filename
                    if attachment_filename in exists_attachments:
                        continue
                    logger.info('try to create the attachment [%s] id=%s', attachment_filename, vsts_id)
                    attachment_content = attachment.get()
                    created_attachment = wit_client.create_attachment(attachment_content, file_name=attachment_filename)
                    logger.info('the attachment [%s] is uploaded url=%s', attachment_filename, created_attachment.url)
                    attachment_doc = []
                    attachment_doc.append(_create_work_item_field_patch_operation(
                        'add',
                        '/relations/-',
                        {
                            'rel': 'AttachedFile',
                            'url': created_attachment.url,
                        }
                    )
                    )
                    workitem = wit_client.update_work_item(id=vsts_id, document=attachment_doc)
                    logger.info('the  attachment [%s] is created id=%s', attachment_filename, vsts_id)
                # End comments and attachments
                if issue.fields.status.name in STATES:
                    idx = 0
                    for project_state in PROJECT_STATES:
                        idx += 1
                        if workitem.fields['System.State'] == project_state:
                            break
                    for project_state in PROJECT_STATES[idx:]:
                        if workitem.fields['System.State'] == STATES[issue.fields.status.name]:
                            break
                        document = [_create_work_item_field_patch_operation('add', 'System.State', project_state)]
                        old_state = workitem.fields['System.State']
                        logger.debug('%s - try to pass the state from [%s] to [%s]', jira_item, old_state,
                                     project_state)
                        workitem = wit_client.update_work_item(document=document, id=vsts_id)
                        logger.debug('%s - the state is passed from [%s] to [%s]', jira_item, old_state,
                                     workitem.fields['System.State'])

            except:
                logger.error(traceback.format_exc())
                raise click.Abort()

    logger.info('end processing, nbr_issues=%s time=%s seconds', nbr_issues, round(time.time() - start, 2))
    __update_config_file(config, data)


if __name__ == '__main__':
    cli(obj={})


def main():
    return cli(obj={})

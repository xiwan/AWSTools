// CloudWatch Custom Widget sample: display results of Athena queries
const aws = require('aws-sdk')

const DOCS = `
## Run Athena Query
Runs an Athena query and displays results in a table.

### Widget parameters
Param | Description
---|---
**region** | The region to run the Athena query in
**database** | Name of the Athena database
**sql** | The SQL query to run

### Example parameters
\`\`\` yaml
region: ${process.env.AWS_REGION}
database: default
sql: SELECT * FROM cloudfront_logs Limit 10
\`\`\`
`;

const config = require('./config.json');
const CHECK_QUERY_STATUS_DELAY_MS = 250;
const CSS = '<style>td { white-space: nowrap; }</style>'

const sleep = async (delay) => {
    return new Promise((resolve) => setTimeout(resolve, delay));
}

const checkQueryStatus = async (athena, query) => {
    let finished = false;
    while (!finished) {
        await sleep(CHECK_QUERY_STATUS_DELAY_MS);
    
        const response = await athena.getQueryExecution(query).promise();
        const queryStatus = response.QueryExecution.Status.State;
        switch (queryStatus) {
            case 'SUCCEEDED':
                finished = true;
            case 'RUNNING':
            case 'QUEUED':
                continue;
            default:
                console.error('Query Error: ', response);
                throw new Error(`Status of Query ${query.QueryExecutionId} is ${queryStatus}.`);
        }
    }
}

const executeQuery = async (athena, accountId, region, querySQL, database)  => {
    const params = {
        QueryString: querySQL,
        ResultConfiguration: {
            OutputLocation: `s3://aws-cw-widget-athena-query-results-${accountId}-${region}`
        },
        QueryExecutionContext: {
            Database: database
        }
    };
  
    const query = await athena.startQueryExecution(params).promise();
  
    // Wait until query is finished execution.
    await checkQueryStatus(athena, query);
    return await athena.getQueryResults({ QueryExecutionId: query.QueryExecutionId }).promise();
}

const displayResults = async (database, sql, results, region, context) => {
    let html = `
        <form><table>
            <tr>
                <td>Database</td><td><input name="database" value="${database}"></td>
            </tr><tr>
                <td valign=top>SQL</td><td><textarea name="sql" rows="2" cols="80">${sql}</textarea></td>
            </tr>
        </table></form>
        <a class="btn btn-primary">Run query</a>
        <cwdb-action action="call" endpoint="${context.invokedFunctionArn}">{ "region": "${region}" }</cwdb-action>
        <p>
        <h2>Results</h2>
    `;

    if (results && results.ResultSet && results.ResultSet.ResultSetMetadata) {
        const cols = results.ResultSet.ResultSetMetadata.ColumnInfo;
        const rows = results.ResultSet.Rows.slice(1);
        
        html += `
            <table><thead><tr><th>${cols.map(col => col.Label).join('</th><th>')}</th></tr></thead><tbody>`;
  
        rows.forEach(row => {
            html += `<tr><td>${row.Data.map(cell => cell.VarCharValue || '').join('</td><td>')}</td></tr>`;
        });
  
        html += `</tbody></table>`
    } else if (results) {
        html += `<pre>${results}</pre>`;
    }
    
    return html;
};

const getColsAndVals = async (results) => {
    
    let cols_txt = '';
    let rows_txt = ''
    if (results && results.ResultSet && results.ResultSet.ResultSetMetadata) {
        const cols = results.ResultSet.ResultSetMetadata.ColumnInfo;
        const rows = results.ResultSet.Rows.slice(1);
        cols_txt += cols.map(col => col.Label).join('|');
        rows.forEach(row => {
            rows_txt += row.Data.map(cell => cell.VarCharValue || '').join('|>');
        });
    }
    
    return [cols_txt, rows_txt];
}

// 传入cdn的域名或者应用名字 Distribution domain name
const putResultToMetric = async (results, region, sql, database) => {

    const colsAndVals = await getColsAndVals(results);

    const dashboardName = config.cloudWatch.dashboardName;
    const cw = new aws.CloudWatch({region});
    const params = {
        MetricData: [
            {
                MetricName: colsAndVals[0], 
                Value: colsAndVals[1], 
                Unit: 'Count',
                Dimensions: [
                    {
                        Name: config.cloudWatch.dimension.name,
                        Value: config.cloudWatch.dimension.value
                    }
                ]
            }
        ],
        Namespace: config.cloudWatch.namespace
    };
    
    cw.putMetricData(params, function(err, data) {
        if (err) console.log(err, err.stack); // an error occurred
        else     console.log(data);           // successful response
        });
}

// MetricName: colsAndVals[0]
// AlarmName 
// AlarmDescription
const createalarm = async (results, region, sql, database) => {

    const colsAndVals = await getColsAndVals(results);
    const snsArn = config.snaArn;
    const cw = new aws.CloudWatch({region});

    const paramsalarm = {
        AlarmNames: [ config.cloudWatch.alarmName ]
    };
    
    cw.describeAlarms(paramsalarm, function(err, data) {
        if (err) {
            console.log("Error", err);
            throw new Error(err);
        } else {
            // List the names of all current alarms in the console
            // console.log(data.MetricAlarms.length);
            if (data.MetricAlarms.length === 0) {
                const params = 
                {
                    "Namespace": cloudWatch.namespace,
                    "MetricName": colsAndVals[0],
                    "Dimensions": [
                        {
                            "Name": config.cloudWatch.dimension.name,
                            "Value": config.cloudWatch.dimension.value
                        }
                    ],
                    "ComparisonOperator": config.cloudWatch.alarm.comparisonOperator,
                    "DatapointsToAlarm": config.cloudWatch.alarm.datapointsToAlarm,
                    "EvaluationPeriods": config.cloudWatch.alarm.evaluationPeriods,
                    "Period": config.cloudWatch.alarm.period,
                    "Statistic": "Average",
                    "Threshold": config.cloudWatch.alarm.threshold,
                    "AlarmDescription": config.cloudWatch.alarm.description,
                    "AlarmName": config.cloudWatch.alarm.name,
                    "AlarmActions": [
                        snsArn
                    ],
                };
        
                //console.log("Create alarm");
                cw.putMetricAlarm(params, function(err, data) {
                    if (err) console.log(err, err.stack); // an error occurred
                    else     console.log(data);           // successful response
                });
               // console.log("Nodata");
            };
       // data.MetricAlarms.forEach(function (item, index, array) {
    //       console.log("find an alarm");
     //      console.log(item.AlarmName);
       //});
        }
    });
}

// metrics 和上面的值一致
const putDashboard = async (results, region, sql, database) => {

    const colsAndVals = await getColsAndVals(results);
    const dashboardName = config.cloudWatch.dashboardName;
    
    let DOCS_TEXT = await genStandardDocText(colsAndVals, region, sql, database);
    
    let final_dashboard_body = {'widgets': []};
    let widget_template_text = {
        "type":"text",
        "x":0,
        "y":7,
        "width":10,
        "height":5,
        "properties":{
            "markdown": DOCS_TEXT
        }
    }

    let widget_template_metric = {
        "type": "metric",
        "x": 0,
        "y": 6,
        "width": 12,
        "height": 6,
        "properties": {
            "metrics": [
                [
                    config.cloudWatch.namespace, //namespace
                    colsAndVals[0],    // metricname
                    config.cloudWatch.dimension.name, // dimensionname
                    config.cloudWatch.dimension.value // dimensionvalue
                ]
            ],
            "period": 300,
            "stat": "Average",
            "region": region,
            "title": dashboardName+"-metric"
        }
    }

    final_dashboard_body.widgets[0] = widget_template_text;
    final_dashboard_body.widgets[1] = widget_template_metric;
    
    const cw = new aws.CloudWatch({region});
    const params = {
        DashboardBody: JSON.stringify(final_dashboard_body), /* required */
        DashboardName: dashboardName /* required */
    };
    cw.putDashboard(params, function(err, data) {
        if (err) console.log(err, err.stack); // an error occurred
        else     console.log(data);           // successful response
    });
    
}

const genStandardDocText = async (colsAndVals, region, sql, database) => {
    let DOCS_TEXT = `
    ## MetaData 
    
    ### Region ${region}
    ### SQL ${sql}
    ### Database ${database}
    
    ## Results
    COL | VAL
    ---|---
    **${colsAndVals[0]}** | ${colsAndVals[1]}
    `;

    return DOCS_TEXT;
};

const sendMessageToSNS = async (results, region, sql, database) => {

    const colsAndVals = await getColsAndVals(results);

    if (parseInt(colsAndVals[1]) <= config.cloudWatch.alarm.threshold)
        return;

    let DOCS_TEXT = await genStandardDocText(colsAndVals, region, sql, database);
    
    let now = new Date().toString();
    var sns = new aws.SNS({region});
    let params = {
        Message: `${DOCS_TEXT} \n \n This was sent: ${now}`,
        Subject: config.snsEmailSubject,
        TopicArn: config.snsArn
    };
    
    //console.log(JSON.stringify(params))

    sns.publish(params, function(err, data) {
        if (err) console.log(err, err.stack); 
        else console.log(data);
    });
}

// main entry
exports.handler = async (event, context) => {
    if (event.describe) {
        return DOCS;   
    }
    
    const region = event.region || process.env.AWS_REGION;
    const accountId = context.invokedFunctionArn.split(":")[4];
    const athena = new aws.Athena({ region });
    const widget = event.hasOwnProperty('widgetContext');
    
    if (widget)
    {
        const form = event.widgetContext.forms.all;
        const database = form.database || event.database || 'default';

        const sql = form.sql || event.sql;
        let results;
        if (database && sql && sql.trim() !== '') {
            try {
                results = await executeQuery(athena, accountId, region, sql, database);
            } catch (e) {
                throw new Error(`execution failed: ${e}.`);
            }
        }
        
        return CSS + await displayResults(database, sql, results, region, context);
    }
    else
    {
        const database = config.database || 'default';
        const sqls = config.sqls;
        for (const item of sqls) {
            const sql = item.statement;
            let results;
            if (database && sql && sql.trim() !== '') {
                try {
                    results = await executeQuery(athena, accountId, region, sql, database);
                } catch (e) {
                    throw new Error(`execution failed: ${e}.`);
                }
            }
            await putResultToMetric(results, region, sql, database);
            await createalarm(results, region, sql, database);
            await putDashboard(results, region, sql, database);
            await sendMessageToSNS(results, region, sql, database)
        }
    }

    return "200";
};


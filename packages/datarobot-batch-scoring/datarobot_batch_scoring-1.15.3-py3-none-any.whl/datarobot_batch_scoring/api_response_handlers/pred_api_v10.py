import operator
import json
from six.moves import zip

from datarobot_batch_scoring.exceptions import UnexpectedKeptColumnCount


def format_data(result, batch, **opts):
    pred_name = opts.get('pred_name')
    keep_cols = opts.get('keep_cols')
    skip_row_id = opts.get('skip_row_id')
    fast_mode = opts.get('fast_mode')
    input_delimiter = opts.get('delimiter')

    single_row = result[0]
    fields = sorted(record['label']
                    for record in single_row['predictionValues'])

    if pred_name is not None:
        out_fields = ['row_id', pred_name]
        # batch scoring returns only positive class for binary tasks if
        # user specified pred_name option, so we eliminate negative
        # result
        if len(fields) == 2 and single_row['prediction'] in fields:
            fields = [fields[-1]]
    else:
        out_fields = ['row_id'] + fields

    pred = [[record['rowId'] + batch.id] + [
        pred_vals['value'] for pred_vals in
        sorted(record['predictionValues'],
               key=operator.itemgetter('label'))
        if pred_vals['label'] in fields]
            for record in sorted(result,
                                 key=operator.itemgetter('rowId'))]

    if keep_cols:
        # stack columns

        feature_indices = {col: i for i, col in
                           enumerate(batch.fieldnames)}
        indices = [feature_indices[col] for col in keep_cols]

        written_fields = []

        if not skip_row_id:
            written_fields.append('row_id')

        written_fields += keep_cols + out_fields[1:]

        # first column is row_id
        comb = []
        for row, predicted in zip(batch.data, pred):
            if fast_mode:
                # row is a full line, we need to cut it into fields
                row = row.rstrip().split(input_delimiter)
                if len(row) != len(batch.fieldnames):
                    raise UnexpectedKeptColumnCount()

            keeps = [row[i] for i in indices]
            output_row = []
            if not skip_row_id:
                output_row.append(predicted[0])
            output_row += keeps + predicted[1:]
            comb.append(output_row)
    else:
        if not skip_row_id:
            comb = pred
            written_fields = out_fields
        else:
            written_fields = out_fields[1:]
            comb = [row[1:] for row in pred]

    prediction_explanations_keys = ('predictionExplanations', 'reasonCodes',
                                    None)

    def _find_prediction_explanations_key():
        return [key for key in prediction_explanations_keys
                if key in single_row or key is None][0]

    prediction_explanations_key = _find_prediction_explanations_key()
    if prediction_explanations_key:
        num_reason_codes = len(single_row[prediction_explanations_key])
        for num in range(1, num_reason_codes + 1):
            written_fields += [
                'explanation_{0}_feature'.format(num),
                'explanation_{0}_strength'.format(num)
            ]
        for in_row, out_row in zip(result, comb):
            reason_codes = []
            for raw_reason_code in in_row[prediction_explanations_key]:
                reason_codes += [
                    raw_reason_code['feature'],
                    raw_reason_code['strength']
                ]
            out_row.extend(reason_codes)

    return written_fields, comb


def unpack_data(request):
    exec_time = float(request['headers']['X-DataRobot-Execution-Time'])
    result = json.loads(request['text'])  # replace with r.content
    elapsed_total_seconds = request['elapsed']
    return result['data'], exec_time, elapsed_total_seconds

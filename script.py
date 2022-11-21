import os
from datetime import datetime
import pandas as pd


def convert_row(row):
    return """
    <LCTO>
      <NUMLOTE>%s</NUMLOTE>
      <NUMLANC>%s</NUMLANC>
      <CODCTACTB>%s</CODCTACTB>
      <CODCONPAR>%s</CODCONPAR>
      <REFERENCIA>%s</REFERENCIA>
      <DTMOV>%s</DTMOV>
      <CODCENCUS>%s</CODCENCUS>
      <VLRLANC>%s</VLRLANC>
      <CODHISTCTB>%s</CODHISTCTB>
      <COMPLHIST>%s</COMPLHIST> 
      <TIPLANC>%s</TIPLANC>
      <VENCIMENTO>%s</VENCIMENTO>
      <NUMDOC>%s</NUMDOC>
      <CODPROJ>%s</CODPROJ>
      <CODEMPORIG>%s</CODEMPORIG>
    </LCTO>""" % (
        row.NUMLOTE, row.NUMLANC, row.CODCTACTB, row.CODCONPAR, row.REFERENCIA,
        row.DTMOV, row.CODCENCUS, row.VLRLANC, row.CODHISTCTB, row.COMPLHIST,
        row.TIPLANC, row.VENCIMENTO, row.NUMDOC, row.CODPROJ, row.CODEMPORIG)


def generate_xml(filename):
    df = pd.read_csv(filename)
    df['VLRLANC'] = df['VLRLANC'].str.strip()
    df['VLRLANC'] = df['VLRLANC'].str.replace(',', '.')
    df['REFERENCIA'] = pd.DatetimeIndex(df['REFERENCIA']).month
    df['DTMOV'] = pd.DatetimeIndex(df['DTMOV']).day
    df['VENCIMENTO'] = pd.to_datetime(df.VENCIMENTO)
    df['VENCIMENTO'] = df['VENCIMENTO'].dt.strftime('%Y%d%m')
    df['NUMLANC'] = range(1, 1 + len(df))

    output_file = f'lancamentos_contabeis_{str(datetime.now())}.xml'
    with open(os.path.join('outputs', output_file), 'w') as f:
        f.write('<LCTOS>')
        f.write(''.join(df.apply(convert_row, axis=1)))
        f.write('\n</LCTOS>')

    return output_file

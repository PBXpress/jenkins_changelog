import html

class JCLHtmlGen():
    @staticmethod
    def wraptag(msg, tag, **kwparams):
        if len(kwparams) > 0:
            for k, v in kwparams.items():
                otparams = [F'{k}="{v}"' for k, v in kwparams.items()]
            tagparams = ' ' + (' '.join(otparams))
        else:
            tagparams = ''
        msg.insert(0, F'<{tag}{tagparams}>')
        msg.append(F'</{tag}>')
        return msg

    @staticmethod
    def genTable(clnames, items, *rowgetters):
        htmldoc = JCLHtmlGen.wraptag([], 'head')

        table = []
        for clname in clnames:
            table.extend(JCLHtmlGen.wraptag([clname,], 'th'))
        JCLHtmlGen.wraptag(table, 'tr')
        for cmt in items:
            row = []
            for cellget in rowgetters:
                cell = cellget(cmt)
                if isinstance(cell, str):
                    cell = [html.escape(cell),]
                else:
                    assert(isinstance(cell, list) or isinstance(cell, tuple))
                    cell = [x for x in cell]
                row.extend(JCLHtmlGen.wraptag(cell, 'td', style = 'vertical-align:top'))
            JCLHtmlGen.wraptag(row, 'tr')
            table.extend(row)
        JCLHtmlGen.wraptag(table, 'tbody')
        JCLHtmlGen.wraptag(table, 'table', style = 'width:100%')
        JCLHtmlGen.wraptag(table, 'body')
        htmldoc.extend(table)
        JCLHtmlGen.wraptag(htmldoc, 'html')
        return htmldoc

if __name__ == '__main__':
    hg = JCLHtmlGen()
    i = 0
    doc = hg.genTable(('Foo', 'Bar', 'Baz'), (1, 2, 3), lambda x: str(x), lambda x: str(x+1), lambda x: str(x + 2))
    print('\n'.join(doc))

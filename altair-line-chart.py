import streamlit as st
import altair as alt
from vega_datasets import data

# streamlitの設定
st.set_page_config(
    page_title="Example Altair Line Charts",  #ページタイトル
    layout="wide",                      #ページをwide modeに
    initial_sidebar_state="expanded"    #サイドバーを表示
)

st.sidebar.write("""
## Example Altair Line Charts
""")

# データサンプルを取得
@st.experimental_memo
def get_data():
    source = data.stocks()
    source = source[source.date.gt("2004-01-01")]
    return source

source = get_data()

# ページトップ
def page_top():
    st.title('Example Altair Line Charts')
    st.write('StreamlitでAltairを使って折れ線グラフを表示する方法を記載しています。')
    st.write('グラフをインタラクティブにする際に所々詰まったので備忘録として書いています。')
    st.write('[Streamlitの公式ドキュメント](https://docs.streamlit.io/library/api-reference/charts/st.altair_chart)にもインタラクティブなグラフを描く方法は書いていますが、若干完成形のイメージが違いました。')
    st.write('作者のプロフィールは[こちら](https://zatsugaku-engineer.com/static/profile/profile.html)です。')

# サンプルデータを表示
def page_sample_data():
    st.header('サンプルデータ')
    st.write("株価の時系列データです。")
    st.write(source)
    st.write(f"""
        ***{type(source)}***  
        ***{source.dtypes}***
    """)

    st.write("使用するサンプルデータを使うために`pip`でライブラリをインストールします。")
    code = '''
pip install altair vega_datasets
    '''
    
    st.code(code, language='bash')
    
    st.write("サンプルデータを取得するコードは以下です。")
    
    code_datasample = '''
import streamlit as st
import altair as alt
from vega_datasets import data

# データサンプルを取得
def get_data():
    source = data.stocks()
    source = source[source.date.gt("2004-01-01")]
    return source

source = get_data()
    '''
    st.code(code_datasample, language='python')

# シンプルな折れ線グラフを表示
def page_chart1():
    st.header('シンプルな折れ線グラフ')
    chart = alt.Chart(source).mark_line().encode(
        x="date:T",
        y="price",
        color="symbol"
    )

    st.altair_chart(chart, use_container_width=True)

    code = '''
chart = alt.Chart(source).mark_line().encode(
    x="date:T",
    y="price",
    color="symbol"
)

st.altair_chart(chart, use_container_width=True)
    '''
    st.code(code, language='python')
    
    st.write("`x=\"date:T\"`の`:T`は時間や日付の場合は付けておかないと表示が変になる場合があります。")
    st.markdown("詳細は[Altairのドキュメント](https://altair-viz.github.io/user_guide/encoding.html#encoding-data-types)を参考にしてください。")
    
    # グラフの凡例の並び順をデータテーブル通りにしたい場合
    st.subheader('グラフの凡例の並び順をデータテーブル通りにしたい場合')
    st.write("デフォルトでは、凡例の並び順はアルファベット順になる。")
    st.markdown("元のデータの並び順にしたい場合は`color=alt.Color(\"symbol\", sort=None)`とします。")
    
    chart = alt.Chart(source).mark_line().encode(
        x="date:T",
        y="price",
        color=alt.Color("symbol", sort=None)
    )

    st.altair_chart(chart, use_container_width=True)
    
    code = '''
chart = alt.Chart(source).mark_line().encode(
    x="date:T",
    y="price",
    color=alt.Color("symbol", sort=None)
)

st.altair_chart(chart, use_container_width=True)
    '''
    st.code(code, language='python')
    
# 凡例をクリックして表示するグラフを選択
def page_chart2():
    st.header('凡例をクリックして表示グラフを選択')
    st.write("凡例をクリックすると、選択したグラフのみ色が濃くなります。")
    st.write("凡例以外のどこかをクリックすると、全表示されます。")
    
    selection = alt.selection_multi(fields=['symbol'], bind='legend')
    chart = alt.Chart(source).mark_line().encode(
        x="date:T",
        y="price",
        color="symbol",
        opacity=alt.condition(selection, alt.value(1), alt.value(0.1))
        ).add_selection(
            selection
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    code = '''
selection = alt.selection_multi(fields=['symbol'], bind='legend')
chart = alt.Chart(source).mark_line().encode(
    x="date:T",
    y="price",
    color="symbol",
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1))
    ).add_selection(
        selection
)

st.altair_chart(chart, use_container_width=True)
    '''
    st.code(code, language='python')
    
# ホバー時にマーカーとツールチップを表示
def page_chart3():
    st.header('ホバー時にマーカーとツールチップを表示')
    st.write("グラフをホバーすると近くのデータの情報が表示されます。")
    
    selection = alt.selection_multi(fields=['symbol'], bind='legend')
    chart = alt.Chart(source).mark_line().encode(
        x="date:T",
        y="price",
        color="symbol",
        opacity=alt.condition(selection, alt.value(1), alt.value(0.1))
        ).add_selection(
            selection
    )
        
    # ホバー時にマーカーを表示する
    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    chart_temp = (
        alt.Chart(source)
        .encode(
            x="date:T",
            y="price",
            color="symbol",
        )
    )
    points = chart_temp.transform_filter(hover).mark_circle(size=50)

    # ホバー時にツールチップを表示
    tooltips = (
        alt.Chart(source)
        .mark_rule()
        .encode(
            x="date:T",
            y="price",
            opacity=alt.condition(hover, alt.value(0.1), alt.value(0)),
            tooltip=[
                alt.Tooltip("date:T", title="date"),
                alt.Tooltip("price", title="price"),
                alt.Tooltip("symbol", title="symbol"),
            ],
        )
        .add_selection(hover)
    )
        
    st.altair_chart((chart + points + tooltips).interactive(), use_container_width=True)
    
    code = '''
selection = alt.selection_multi(fields=['symbol'], bind='legend')
chart = alt.Chart(source).mark_line().encode(
    x="date:T",
    y="price",
    color="symbol",
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1))
    ).add_selection(
        selection
)
    
# ホバー時にマーカーを表示する
hover = alt.selection_single(
    fields=["date"],
    nearest=True,
    on="mouseover",
    empty="none",
)
chart_temp = (
    alt.Chart(source)
    .encode(
        x="date:T",
        y="price",
        color="symbol",
    )
)
points = chart_temp.transform_filter(hover).mark_circle(size=50)

# ホバー時にツールチップを表示
tooltips = (
    alt.Chart(source)
    .mark_rule()
    .encode(
        x="date:T",
        y="price",
        opacity=alt.condition(hover, alt.value(0.1), alt.value(0)),
        tooltip=[
            alt.Tooltip("date:T", title="date"),
            alt.Tooltip("price", title="price"),
            alt.Tooltip("symbol", title="symbol"),
        ],
    )
    .add_selection(hover)
)
    
st.altair_chart((chart + points + tooltips).interactive(), use_container_width=True)
    '''
    st.code(code, language='python')

# ページ切り替え
page_name = st.sidebar.selectbox(
     'ページを選択',
     ('トップ', 'サンプルデータ', 'シンプルな折れ線グラフ', '凡例をクリックして表示グラフ選択', 'ホバー時にマーカーとツールチップを表示')
)

if page_name == 'トップ':
   page_top()
elif page_name == 'サンプルデータ':
   page_sample_data()
elif page_name == 'シンプルな折れ線グラフ':
   page_chart1()
   
elif page_name == '凡例をクリックして表示グラフ選択':
   page_chart2()
   
elif page_name == 'ホバー時にマーカーとツールチップを表示':
   page_chart3()
else:
    st.write("エラー")
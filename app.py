import streamlit as st
import streamlit.components.v1 as components
# import networkx as nx
# from pyvis.network import Network
# from networkmap.pipeline import pipeline
from pyvis.network import Network
from io import StringIO
import re
import asyncio
from local import local_graph


FILE = "pcap_files/network.pcap"
st.set_page_config(layout='wide')
st.title('Network Graph Map Visualization')
st.sidebar.header('Upload Network Dump')
uploaded_file = st.sidebar.file_uploader(":blue[Upload Here:]", type=['pcap', 'txt'])
clean_data = None

if uploaded_file:
    # with open(FILE, "wb") as binary_file:
    #     # Write bytes to file
    #     binary_file.write(uploaded_file.getvalue())
    # with open(FILE, 'rb') as fobj:
    #     response = requests.post("http://localhost:8080/pcap", files={'file': fobj})

    st.sidebar.markdown("""---""")
    st.sidebar.header('Graph management')

    if st.sidebar.button('Get NetFrenzy Graph'):
        with st.spinner("Please Wait..."):
            # t = "http://127.0.0.1:7474/browser/"
            st.components.v1.iframe("http://localhost:8000/NetFrenzy.html", height=800, scrolling=True)

    if st.sidebar.button('Get Urls Graph'):
        st.components.v1.iframe(" http://localhost:8888/index.html", height=800, scrolling=True)

    if st.sidebar.button('Get Local Graph'):
        local_graph()
    #
    #
    #     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    #     string_data = stringio.readlines()
    #     clean_data = [re.sub(r'[\n\r]', "", line) for line in string_data]
    #     ip = st.text_input("IP of the centre node (Optional)", help="The IP address where the dumpfile was taken; "
    #                                                                 "default: tries to guess based on the content of the file")
    #     default_type = ''
    #     type_options = [default_type, 'arp', 'route', 'traceroute']
    #     type_ind = type_options.index(default_type)
    #     dumpfile_type = st.selectbox("Dumpfile Type (Optional)", options=type_options, index=type_ind,
    #                                  help="Dumpfile type; default: tries to guess based on file format")
    #     default_os = ''
    #     os_options = [default_os, 'linux', 'windows', 'openbsd']
    #     od_ind = os_options.index(default_os)
    #     dumpfile_os = st.selectbox("Operating System (Optional)", options=os_options, index=od_ind,
    #                                help="Operating System; default: tries to guess")
    #     new_graph = st.checkbox(label="Is New Graph?", value=True)
    #     physics = st.checkbox(label='Add Physics Interactivity?', value=False)
    #     is_generate = st.button("Generate Graph")
    #     if is_generate:
    #         dumpfile_os = dumpfile_os if dumpfile_os != default_os else None
    #         dumpfile_type = dumpfile_type if dumpfile_type != default_type else None
    #         g = pipeline(clean_data, ip=ip, dumpfile_type=dumpfile_type, dumpfile_os=dumpfile_os, new_graph=new_graph)
    #         # Initiate PyVis network object
    #         nt = Network(
    #             height='400px',
    #             width='100%',
    #             bgcolor='#222222',
    #             font_color='white'
    #         )
    #
    #         # Take Networkx graph and translate it to a PyVis graph format
    #         nt.from_nx(g)
    #
    #         # Generate network with specific layout settings
    #         nt.repulsion(
    #             node_distance=420,
    #             central_gravity=0.33,
    #             spring_length=110,
    #             spring_strength=0.10,
    #             damping=0.95
    #         )
    #
    #         # Save and read graph as HTML file (on Streamlit Sharing)
    #
    #         # Save and read graph as HTML file (locally)
    #         if physics:
    #             nt.show_buttons(filter_=['physics'])
    #         nt.save_graph(r'C:\Users\Itay Gafni\Projects\NetworkMap\html_files\pyvis_network_graph.html')
    #         HtmlFile = open(r'C:\Users\Itay Gafni\Projects\NetworkMap\html_files\pyvis_network_graph.html', 'r',
    #                         encoding='utf-8')
    #         # Load HTML file in HTML component for display on Streamlit page
    #         components.html(HtmlFile.read(), height=900, width=900)

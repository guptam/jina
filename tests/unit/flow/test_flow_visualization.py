import os
import numpy as np
from PIL import Image
from jina.flow import Flow


def test_visualization_URL():
    flow = (Flow().add(name='pod_a')
            .add(name='pod_b', needs='gateway')
            .join(needs=['pod_a', 'pod_b']))
    url = flow.plot()
    url_split = url.split("view/") #check that has info after standard URL text

    assert url_split[1] is not ' '


def test_visualization_with_yml_file_img(tmpdir):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    tmpfile = os.path.join(tmpdir, 'flow_test.jpg')

    flow = Flow.load_config(os.path.join(cur_dir, '../yaml/test_flow_visualization.yml')).plot(output=tmpfile)

   with Image.open(os.path.join(cur_dir, 'flow_original_test.jpg')) as flow_original:
        with Image.open(tmpfile) as flow_created:
            assert flow_original.size == flow_created.size
            np.testing.assert_array_almost_equal(flow_original, flow_created)

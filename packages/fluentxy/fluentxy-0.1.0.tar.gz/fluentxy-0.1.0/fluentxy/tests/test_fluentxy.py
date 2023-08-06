from .. import parse_data
import pytest

pd = pytest.importorskip("pandas")
pdt = pytest.importorskip("pandas.util.testing")


def test_parse_data(shared_datadir):
    with open(shared_datadir / "axial-velocity-mesh-1.xy") as m:
        mesh_1 = m.readlines()
    mesh_1_data = parse_data(mesh_1)
    mesh_1_csv = pd.read_csv(
        shared_datadir / "axial-velocity-mesh-1.csv", header=[0, 1], index_col=0
    )
    pdt.assert_frame_equal(mesh_1_data, mesh_1_csv, check_names=True)

    with open(shared_datadir / "axial-velocity-mesh-2.xy") as m:
        mesh_2 = m.readlines()
    mesh_2_data = parse_data(mesh_2)
    mesh_2_csv = pd.read_csv(
        shared_datadir / "axial-velocity-mesh-2.csv", header=[0, 1], index_col=0
    )
    pdt.assert_frame_equal(mesh_2_data, mesh_2_csv, check_names=True)

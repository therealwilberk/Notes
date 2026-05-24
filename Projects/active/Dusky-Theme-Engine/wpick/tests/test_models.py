from __future__ import annotations

from wpick.models import (
    AssignerError,
    ClusterError,
    ClusterRow,
    ConfigError,
    DatabaseError,
    ExtractorError,
    FeatureRow,
    OklabColor,
    OrchestratorError,
    PickerError,
    WpickError,
)


class TestExceptionHierarchy:
    def test_wpick_error_is_base(self) -> None:
        assert issubclass(ExtractorError, WpickError)
        assert issubclass(ClusterError, WpickError)
        assert issubclass(AssignerError, WpickError)
        assert issubclass(OrchestratorError, WpickError)
        assert issubclass(PickerError, WpickError)
        assert issubclass(DatabaseError, WpickError)
        assert issubclass(ConfigError, WpickError)

    def test_exceptions_carry_message(self) -> None:
        for exc_type in (
            ExtractorError,
            ClusterError,
            AssignerError,
            OrchestratorError,
            PickerError,
            DatabaseError,
            ConfigError,
        ):
            exc = exc_type("test message")
            assert str(exc) == "test message"
            assert isinstance(exc, Exception)


class TestOklabColor:
    def test_init(self) -> None:
        c = OklabColor(L=0.5, a=0.3, b=0.1)
        assert c.L == 0.5
        assert c.a == 0.3
        assert c.b == 0.1

    def test_floats(self) -> None:
        c = OklabColor(0.0, 0.0, 0.0)
        assert isinstance(c.L, float)


class TestFeatureRow:
    def test_fields(self) -> None:
        row = FeatureRow(
            image_id="abc",
            path="/img.png",
            oklab_vector=[0.1, 0.2],
            color_count=2,
            extracted_at="2026-01-01T00:00:00",
        )
        assert row.image_id == "abc"
        assert row.oklab_vector == [0.1, 0.2]
        assert row.extracted_at == "2026-01-01T00:00:00"


class TestClusterRow:
    def test_fields(self) -> None:
        row = ClusterRow(
            cluster_id=1,
            label="warm",
            centroid=[0.5, 0.5],
            member_count=5,
            run_id="run1",
        )
        assert row.cluster_id == 1
        assert row.label == "warm"
        assert row.member_count == 5

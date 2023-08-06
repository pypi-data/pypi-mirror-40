# Change Log

All notable changes to this project are documented in this file.

## [1.0.6] - 2019-01-10
- Fixed issue in the MATPOWER import with optional data columns of the MATPOWER format.

## [1.0.5] - 2019-01-10
- Added ``Scenario.has_hybrid_architecture``, ``Scenario.get_ac_branches``, ``Scenario.get_dc_branches``, ``Scenario.add_compensator``, ``CapRegion.copy``, ``show_power_balance_error``, and ``show_branch_reconstruction_error``.
- Added an object-oriented design to the rank-1 approximation methods (to avoid the need of closures for their configuration).
- Added the detection of omitted ramping limits in the MATPOWER import.
- Extended the physical validity assessment that underlies ``OPFResult.is_physical``.
- Updated the automatic solver selection and OPF result summary with the consideration of the *hybrid architecture*.
- Changed the default rank-1 approximation to the graph traversal method.
- Removed ``SystemModel.is_acyclic``, ``SystemModel.ac_subgrids``, and ``SystemModel.dc_subgrids``.

## [1.0.4] - 2018-12-28
- Revised the constraint scaling to improve performance.

## [1.0.3] - 2018-12-11
- Extended the scenario verification to detect lines that connect buses with different base voltages.

## [1.0.2] - 2018-12-07
- Revised the management of worker processes to improve performance, especially under Windows.

## [1.0.1] - 2018-11-29
- Updated the README with solver installation instructions for Windows.
- Excluded support for CVXPY.

## [1.0.0] - 2018-11-27
- Official release.

## [0.9.9] - 2018-11-26
- Initial commit to GitLab.com.

## [0.9.8] - 2018-10-19
- Pre-release of *hynet* on PyPI.

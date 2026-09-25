# ISM coverage matrix

Generated from [`../coverage.yaml`](../coverage.yaml) (ISM 2026-06); do not edit.

131 controls reviewed for Kubernetes platforms. Each row says where the evidence
lives and how far this project produces it. It does not say who is responsible: join that from
the provider's controls matrix with `scripts/import_cscm.py`. On EKS Fargate, the node layer
moves to the provider.

## Summary

Controls spanning several layers count once in each.

| Coverage | Workload | Cluster | Node | AWS account | Identity | Organisation | Endpoint | Provider | Controls |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| automated | 15 | 6 | 5 | 3 |  |  |  | 1 | 21 |
| buildable | 6 | 26 | 17 | 24 |  |  |  | 4 | 43 |
| external-api |  |  |  |  | 22 |  |  |  | 22 |
| document |  |  |  |  |  | 15 |  |  | 15 |
| provider-report |  |  |  |  |  |  |  | 4 | 4 |
| outside-platform |  |  |  |  |  |  | 26 |  | 26 |

## Automated: a detector in this project produces evidence

| ISM ID | Layers | Collectors | Control |
|---|---|---|---|
| ISM-0445 | Cluster | — | Privileged users are assigned a dedicated privileged user account to be used solely for duties requiring privileged access. |
| ISM-1182 | Cluster, AWS account | — | Network access controls are implemented to limit the flow of network traffic within and between network segments to only that required for business purposes. |
| ISM-1246 | Workload | — | Server applications are hardened using ASD and vendor hardening guidance, with the most restrictive guidance taking precedence when conflicts occur. |
| ISM-1416 | Cluster, AWS account | — | A software firewall is implemented on workstations and servers to restrict inbound and outbound network connections to an organisation-approved set of applications and services. |
| ISM-1490 | Workload | — | Application control is implemented on internet-facing servers. |
| ISM-1501 | Workload, Node | — | Operating systems that are no longer supported by vendors are replaced. |
| ISM-1511 | Cluster, AWS account | — | Backups of data, applications and settings are performed and retained in accordance with business criticality and business continuity requirements. |
| ISM-1604 | Workload, Node, Provider | — | When using a software-based isolation mechanism that consumes shared physical computing resources, the configuration of the isolation mechanism is hardened by removing unneeded functionality and restricting access to the administrative interface used to manage the isolation mechanism. |
| ISM-1657 | Workload | — | Application control restricts the execution of executables, libraries, scripts, installers, compiled HTML, HTML applications and control panel applets to an organisation-approved set. |
| ISM-1685 | Cluster | — | Credentials for break glass accounts, local administrator accounts and service accounts are long, unique, unpredictable and managed. |
| ISM-1690 | Workload | — | Patches, updates or other vendor mitigations for vulnerabilities in online services are applied within two weeks of release when vulnerabilities are assessed as non-critical by vendors and no working exploits exist. |
| ISM-1693 | Workload | — | Patches, updates or other vendor mitigations for vulnerabilities in applications other than office productivity suites, web browsers and their extensions, email clients, PDF applications, and security products are applied within one month of release. |
| ISM-1694 | Workload, Node | — | Patches, updates or other vendor mitigations for vulnerabilities in operating systems of internet-facing servers and internet-facing network devices are applied within two weeks of release when vulnerabilities are assessed as non-critical by vendors and no working exploits exist. |
| ISM-1695 | Workload, Node | — | Patches, updates or other vendor mitigations for vulnerabilities in operating systems of workstations, non-internet-facing servers and non-internet-facing network devices are applied within one month of release. |
| ISM-1698 | Workload | — | A vulnerability scanner is used at least daily to identify missing patches or updates for vulnerabilities in online services. |
| ISM-1700 | Workload | — | A vulnerability scanner is used at least fortnightly to identify missing patches or updates for vulnerabilities in applications other than office productivity suites, web browsers and their extensions, email clients, PDF applications, and security products. |
| ISM-1808 | Workload | — | A vulnerability scanner with an up-to-date vulnerability database is used for vulnerability scanning activities. |
| ISM-1871 | Workload | — | Application control is applied to all locations other than user profiles and temporary folders used by operating systems, web browsers and email clients. |
| ISM-1876 | Workload | — | Patches, updates or other vendor mitigations for vulnerabilities in online services are applied within 48 hours of release when vulnerabilities are assessed as critical by vendors or when working exploits exist. |
| ISM-1877 | Workload, Node | — | Patches, updates or other vendor mitigations for vulnerabilities in operating systems of internet-facing servers and internet-facing network devices are applied within 48 hours of release when vulnerabilities are assessed as critical by vendors or when working exploits exist. |
| ISM-1883 | Cluster | — | Privileged user accounts explicitly authorised to access online services are strictly limited to only what is required for users and services to undertake their duties. |

## Buildable: technical evidence can be collected; no detector yet

| ISM ID | Layers | Collectors | Control |
|---|---|---|---|
| ISM-0298 | Node | node-inventory | A centralised and managed approach that maintains the integrity of patches or updates, and confirms that they have been applied successfully, is used to patch or update applications, operating systems, drivers and firmware. |
| ISM-0459 | Cluster, AWS account | aws-account | Full disk encryption, or partial encryption where access controls only allow writing to encrypted partitions or volumes, is implemented when encrypting media. |
| ISM-0469 | Cluster, AWS account | kyverno, aws-account | An AACP or high assurance cryptographic protocol is used when encrypting data in transit. |
| ISM-0471 | Cluster, AWS account | kyverno, aws-account | Only AACAs or high assurance cryptographic algorithms are used by cryptographic equipment, applications and libraries. |
| ISM-0585 | Cluster, AWS account | aws-account | For each event logged, the date and time of the event, the relevant user or process, the relevant filename, the event description, and the information technology equipment involved are captured. |
| ISM-0988 | Cluster, AWS account | node-host | An accurate and consistent time source is used for event logging. |
| ISM-1080 | Cluster, AWS account | aws-account | An AACA or high assurance cryptographic algorithm is used when encrypting data at rest. |
| ISM-1405 | Cluster, AWS account | aws-account | A centralised event logging facility is implemented. |
| ISM-1409 | Node | node-host | Operating systems are hardened using ASD and vendor hardening guidance, with the most restrictive guidance taking precedence when conflicts occur. |
| ISM-1509 | Cluster, Node, AWS account | aws-account | Privileged access events are centrally logged. |
| ISM-1605 | Node, Provider | node-host | When using a software-based isolation mechanism that consumes shared physical computing resources, the underlying operating system is hardened. |
| ISM-1606 | Node, Provider | node-host | When using a software-based isolation mechanism that consumes shared physical computing resources, patches, updates or vendor mitigations for vulnerabilities are applied to the isolation mechanism and underlying operating system in a timely manner. |
| ISM-1607 | Node, Provider | node-host | When using a software-based isolation mechanism that consumes shared physical resources, integrity monitoring and centralised event logging is performed for the isolation mechanism and underlying operating system. |
| ISM-1643 | Cluster, Node | node-inventory | Software registers contain versions and patch histories of applications, drivers, operating systems and firmware. |
| ISM-1650 | Cluster, Node, AWS account | aws-account | Privileged user account and security group management events are centrally logged. |
| ISM-1660 | Cluster, Node, AWS account | kyverno, aws-account | Allowed and blocked application control events are centrally logged. |
| ISM-1696 | Node | node-inventory | Patches, updates or other vendor mitigations for vulnerabilities in operating systems of workstations, non-internet-facing servers and non-internet-facing network devices are applied within 48 hours of release when vulnerabilities are assessed as critical by vendors or when working exploits exist. |
| ISM-1701 | Node | aws-account | A vulnerability scanner is used at least daily to identify missing patches or updates for vulnerabilities in operating systems of internet-facing servers and internet-facing network devices. |
| ISM-1702 | Node | aws-account | A vulnerability scanner is used at least fortnightly to identify missing patches or updates for vulnerabilities in operating systems of workstations, non-internet-facing servers and non-internet-facing network devices. |
| ISM-1705 | Cluster, AWS account | kyverno, aws-account | Privileged user accounts (excluding backup administrator accounts) cannot access backups belonging to other user accounts. |
| ISM-1707 | Cluster, AWS account | kyverno, aws-account | Privileged user accounts (excluding backup administrator accounts) are prevented from modifying and deleting backups. |
| ISM-1708 | Cluster, AWS account | aws-account | Backup administrator accounts are prevented from modifying and deleting backups during their retention period. |
| ISM-1787 | Workload | kyverno | Operating systems, applications, IT equipment, OT equipment and services are sourced from approved suppliers. |
| ISM-1791 | Workload | kyverno | The integrity of operating systems, applications, IT equipment, OT equipment and services are assessed as part of acceptance of products and services. |
| ISM-1792 | Workload | kyverno | The authenticity of operating systems, applications, IT equipment, OT equipment and services are assessed as part of acceptance of products and services. |
| ISM-1807 | Cluster, Node | node-inventory, aws-account | An automated method of asset discovery is used at least fortnightly to support the detection of assets for subsequent vulnerability scanning activities. |
| ISM-1810 | Cluster, AWS account | aws-account | Backups of data, applications and settings are synchronised to enable restoration to a common point in time. |
| ISM-1811 | Cluster, AWS account | aws-account | Backups of data, applications and settings are retained in a secure and resilient manner. |
| ISM-1812 | Cluster, AWS account | kyverno, aws-account | Unprivileged user accounts cannot access backups belonging to other user accounts. |
| ISM-1814 | Cluster, AWS account | kyverno, aws-account | Unprivileged user accounts are prevented from modifying and deleting backups. |
| ISM-1815 | Cluster, AWS account | aws-account | Event logs are protected from unauthorised modification and deletion. |
| ISM-1848 | Node, Provider | node-host | When using a software-based isolation mechanism that consumes shared physical computing resources, the isolation mechanism or underlying operating system is replaced when it is no longer supported by a vendor. |
| ISM-1889 | Cluster, Node, AWS account | aws-account | Command line process creation events are centrally logged. |
| ISM-1902 | Node | node-inventory | Patches, updates or other vendor mitigations for vulnerabilities in operating systems of workstations, non-internet-facing servers and non-internet-facing network devices are applied within one month of release when vulnerabilities are assessed as non-critical by vendors and no working exploits exist. |
| ISM-1905 | Workload | — | Online services that are no longer supported by vendors are removed. |
| ISM-1959 | Cluster, AWS account | aws-account | To the extent possible, event logs are captured and stored in a consistent and structured format. |
| ISM-1977 | Node | aws-account | Security-relevant events for Linux operating systems are centrally logged. |
| ISM-1983 | Cluster, AWS account | aws-account | Event logs sent to a centralised event logging facility are sent as soon as possible after they occur. |
| ISM-1984 | Cluster, AWS account | aws-account | Event logs sent to a centralised event logging facility are encrypted in transit using Australian Signals Directorate (ASD)-approved cryptography. |
| ISM-1985 | Cluster, AWS account | aws-account | Event logs are protected from unauthorised access. |
| ISM-1988 | Cluster, AWS account | aws-account | Event logs are retained in a searchable manner for at least 12 months. |
| ISM-2051 | Workload | — | Software generates sufficient event logs to support the detection of cyber security events. |
| ISM-2052 | Workload | — | Event logs produced by software ensure that any sensitive data is protected. |

## External API: collectable from identity or account systems outside the cluster

| ISM ID | Layers | Collectors | Control |
|---|---|---|---|
| ISM-0974 | Identity | identity-provider | Multi-factor authentication is used to authenticate unprivileged users of systems. |
| ISM-1173 | Identity | identity-provider | Multi-factor authentication is used to authenticate privileged users of systems. |
| ISM-1175 | Identity | identity-provider, aws-account | Privileged user accounts (excluding those explicitly authorised to access online services) are prevented from accessing the internet, email and web services. |
| ISM-1380 | Identity | identity-provider, aws-account | Privileged users use separate privileged and unprivileged operating environments. |
| ISM-1387 | Identity | identity-provider, aws-account | Administrative activities are conducted through jump servers. |
| ISM-1401 | Identity | identity-provider | Multi-factor authentication uses either: something users have and something users know, or something users have that is unlocked by something users know or are. |
| ISM-1504 | Identity | identity-provider | Multi-factor authentication is used to authenticate users to their organisation’s online services that process, store or communicate their organisation’s sensitive data. |
| ISM-1507 | Identity | identity-provider | Requests for privileged access to systems and their resources are validated when first requested. |
| ISM-1647 | Identity | identity-provider | Privileged access to systems and their resources are disabled after 12 months unless revalidated. |
| ISM-1648 | Identity | identity-provider | Privileged access to systems and their resources are disabled after 45 days of inactivity. |
| ISM-1679 | Identity | identity-provider | Multi-factor authentication is used to authenticate users to third-party online services that process, store or communicate their organisation’s sensitive data. |
| ISM-1680 | Identity | identity-provider | Multi-factor authentication (where available) is used to authenticate users to third-party online services that process, store or communicate their organisation’s non-sensitive data. |
| ISM-1681 | Identity | identity-provider | Multi-factor authentication is used to authenticate customers to online customer services that process, store or communicate sensitive customer data. |
| ISM-1682 | Identity | identity-provider | Multi-factor authentication used for authenticating users of systems is phishing-resistant. |
| ISM-1683 | Identity | identity-provider | Successful and unsuccessful multi-factor authentication events are centrally logged. |
| ISM-1687 | Identity | identity-provider, aws-account | Privileged operating environments are not virtualised within unprivileged operating environments. |
| ISM-1688 | Identity | identity-provider, aws-account | Unprivileged user accounts cannot logon to privileged operating environments. |
| ISM-1689 | Identity | identity-provider, aws-account | Privileged user accounts (excluding local administrator accounts) cannot logon to unprivileged operating environments. |
| ISM-1872 | Identity | identity-provider | Multi-factor authentication used for authenticating users of online services is phishing-resistant. |
| ISM-1873 | Identity | identity-provider | Multi-factor authentication used for authenticating customers of online customer services provides a phishing-resistant option. |
| ISM-1892 | Identity | identity-provider | Multi-factor authentication is used to authenticate users to their organisation’s online customer services that process, store or communicate their organisation’s sensitive customer data. |
| ISM-1893 | Identity | identity-provider | Multi-factor authentication is used to authenticate users to third-party online customer services that process, store or communicate their organisation’s sensitive customer data. |

## Document: needs an organisational record; attach evidence

| ISM ID | Layers | Collectors | Control |
|---|---|---|---|
| ISM-0041 | Organisation | — | Systems have a system security plan that includes an overview of the system (covering the system’s purpose, the system boundary and how the system is managed) as well as an annex that covers applicable controls from this document and any additional controls that have been identified and implemented. |
| ISM-0043 | Organisation | — | Systems have a cyber security incident response plan that covers the following: |
| ISM-0123 | Organisation | — | Cyber security incidents are reported to the chief information security officer, or one of their delegates, as soon as possible after they occur or are discovered. |
| ISM-0140 | Organisation | — | Cyber security incidents are reported to ASD as soon as possible after they occur or are discovered. |
| ISM-0507 | Organisation | — | Cryptographic key management processes, and supporting cryptographic key management procedures, are developed, implemented and maintained. |
| ISM-0580 | Organisation | — | A security monitoring policy is developed, implemented and maintained. |
| ISM-1228 | Organisation | — | Cyber security events are analysed in a timely manner to identify cyber security incidents. |
| ISM-1515 | Organisation | — | Restoration of data, applications and settings from backups to a common point in time is tested as part of disaster recovery exercises. |
| ISM-1547 | Organisation | — | Data backup processes, and supporting data backup procedures, are developed, implemented and maintained. |
| ISM-1582 | Organisation | — | Application control rulesets are validated at least annually. |
| ISM-1809 | Organisation | — | When applications, operating systems, network devices or networked IT equipment that are no longer supported by vendors cannot be immediately removed or replaced, compensating controls are implemented until such time that they can be removed or replaced. |
| ISM-1819 | Organisation | — | Following the identification of a cyber security incident, the cyber security incident response plan is enacted. |
| ISM-1906 | Organisation | — | Event logs from internet-facing servers are analysed in a timely manner to detect cyber security events. |
| ISM-1986 | Organisation | — | Event logs from critical servers are analysed in a timely manner to detect cyber security events. |
| ISM-1989 | Organisation | — | Event logs are retained as per minimum retention requirements for various classes of records as set out by the National Archives of Australia’s Administrative Functions Disposal Authority Express (AFDA Express) Version 2 publication. |

## Provider report: cite the provider's assessment

| ISM ID | Layers | Collectors | Control |
|---|---|---|---|
| ISM-0813 | Provider | — | Server rooms, communications rooms and security containers are not left in unsecured states. |
| ISM-1053 | Provider | — | Classified servers, network devices and cryptographic equipment are secured in server rooms or communications rooms that meet the requirements for a security zone suitable for their classification. |
| ISM-1074 | Provider | — | Keys or equivalent access mechanisms to server rooms, communications rooms and security containers are appropriately controlled. |
| ISM-1974 | Provider | — | Non-classified servers, network devices and cryptographic equipment are secured in suitably secure server rooms or communications rooms. |

## Outside platform: endpoint and workstation controls, not part of a Linux cluster

| ISM ID | Layers | Collectors | Control |
|---|---|---|---|
| ISM-0843 | Endpoint | — | Application control is implemented on workstations. |
| ISM-1412 | Endpoint | — | Web browsers are hardened using ASD and vendor hardening guidance, with the most restrictive guidance taking precedence when conflicts occur. |
| ISM-1485 | Endpoint | — | Web browsers do not process web advertisements from the internet. |
| ISM-1486 | Endpoint | — | Web browsers do not process Java from the internet. |
| ISM-1488 | Endpoint | — | Microsoft Office macros in files originating from the internet are blocked. |
| ISM-1489 | Endpoint | — | Microsoft Office macro security settings cannot be changed by users. |
| ISM-1542 | Endpoint | — | Microsoft Office is configured to prevent activation of Object Linking and Embedding packages. |
| ISM-1544 | Endpoint | — | Microsoft’s recommended application blocklist is implemented. |
| ISM-1585 | Endpoint | — | Web browser security settings cannot be changed by users. |
| ISM-1623 | Endpoint | — | PowerShell module logging, script block logging and transcription events are centrally logged. |
| ISM-1654 | Endpoint | — | Internet Explorer 11 is disabled or removed. |
| ISM-1667 | Endpoint | — | Microsoft Office is blocked from creating child processes. |
| ISM-1668 | Endpoint | — | Microsoft Office is blocked from creating executable content. |
| ISM-1669 | Endpoint | — | Microsoft Office is blocked from injecting code into other processes. |
| ISM-1670 | Endpoint | — | PDF applications are blocked from creating child processes. |
| ISM-1671 | Endpoint | — | Microsoft Office macros are disabled for users that do not have a demonstrated business requirement. |
| ISM-1672 | Endpoint | — | Microsoft Office macro antivirus scanning is enabled. |
| ISM-1673 | Endpoint | — | Microsoft Office macros are blocked from making Win32 API calls. |
| ISM-1691 | Endpoint | — | Patches, updates or other vendor mitigations for vulnerabilities in office productivity suites, web browsers and their extensions, email clients, PDF applications, and security products are applied within two weeks of release. |
| ISM-1699 | Endpoint | — | A vulnerability scanner is used at least weekly to identify missing patches or updates for vulnerabilities in office productivity suites, web browsers and their extensions, email clients, PDF applications, and security products. |
| ISM-1704 | Endpoint | — | Office productivity suites, web browsers and their extensions, email clients, PDF applications, Adobe Flash Player, and security products that are no longer supported by vendors are removed. |
| ISM-1823 | Endpoint | — | Office productivity suite security settings cannot be changed by users. |
| ISM-1824 | Endpoint | — | PDF application security settings cannot be changed by users. |
| ISM-1859 | Endpoint | — | Office productivity suites are hardened using ASD and vendor hardening guidance, with the most restrictive guidance taking precedence when conflicts occur. |
| ISM-1860 | Endpoint | — | PDF applications are hardened using ASD and vendor hardening guidance, with the most restrictive guidance taking precedence when conflicts occur. |
| ISM-1870 | Endpoint | — | Application control is applied to user profiles and temporary folders used by operating systems, web browsers and email clients. |

-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 02, 2026 at 02:41 PM
-- Server version: 8.4.3
-- PHP Version: 8.3.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_multimedia`
--

-- --------------------------------------------------------

--
-- Table structure for table `hasil_dokumentasi`
--

CREATE TABLE `hasil_dokumentasi` (
  `id_dokumentasi` int NOT NULL,
  `id_pemesanan` int NOT NULL,
  `link_file` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `hasil_dokumentasi`
--

INSERT INTO `hasil_dokumentasi` (`id_dokumentasi`, `id_pemesanan`, `link_file`) VALUES
(1, 1, 'drive.google.com/Seminar_Nasional_Teknologi'),
(2, 3, 'drive.google.com/Workshop_UIUX_Design'),
(3, 4, 'drive.google.com/Seminar_HMP_Farmasi'),
(4, 5, 'drive.google.com/lomba-cerdas-cermat-2026');

-- --------------------------------------------------------

--
-- Table structure for table `jadwal`
--

CREATE TABLE `jadwal` (
  `id_jadwal` int NOT NULL,
  `id_pemesanan` int NOT NULL,
  `id_tim` int NOT NULL,
  `waktu_kegiatan` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `jadwal`
--

INSERT INTO `jadwal` (`id_jadwal`, `id_pemesanan`, `id_tim`, `waktu_kegiatan`) VALUES
(1, 1, 1, '08:00:00'),
(2, 2, 2, '19:00:00'),
(3, 3, 3, '09:00:00'),
(4, 4, 2, '13:00:00'),
(5, 5, 5, '07:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `log_perubahan_pembayaran`
--

CREATE TABLE `log_perubahan_pembayaran` (
  `id_log` int NOT NULL,
  `id_pembayaran` int DEFAULT NULL,
  `total_bayar_lama` decimal(10,2) DEFAULT NULL,
  `total_bayar_baru` decimal(10,2) DEFAULT NULL,
  `status_lama` varchar(20) DEFAULT NULL,
  `status_baru` varchar(20) DEFAULT NULL,
  `waktu_perubahan` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `log_perubahan_pembayaran`
--

INSERT INTO `log_perubahan_pembayaran` (`id_log`, `id_pembayaran`, `total_bayar_lama`, `total_bayar_baru`, `status_lama`, `status_baru`, `waktu_perubahan`) VALUES
(1, 7, 500000.00, 750000.00, 'Pending', 'Berhasil', '2026-11-02 07:24:18'),
(2, 7, 750000.00, 750000.00, 'Berhasil', 'Pending', '2026-11-02 09:52:30'),
(3, 7, 750000.00, 750000.00, 'Pending', 'Pending', '2026-11-02 09:56:42'),
(4, 2, 0.00, 500000.00, 'Pending', 'Berhasil', '2026-11-02 10:02:52');

-- --------------------------------------------------------

--
-- Table structure for table `pembayaran`
--

CREATE TABLE `pembayaran` (
  `id_pembayaran` int NOT NULL,
  `id_pemesanan` int NOT NULL,
  `tanggal_bayar` date DEFAULT NULL,
  `total_bayar` decimal(10,2) NOT NULL,
  `status_transaksi` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `pembayaran`
--

INSERT INTO `pembayaran` (`id_pembayaran`, `id_pemesanan`, `tanggal_bayar`, `total_bayar`, `status_transaksi`) VALUES
(1, 1, '2026-05-02', 500000.00, 'Berhasil'),
(2, 2, '2026-11-02', 500000.00, 'Berhasil'),
(3, 3, '2026-06-26', 750000.00, 'Berhasil'),
(4, 4, '2026-07-02', 1000000.00, 'Berhasil'),
(5, 5, '2026-08-20', 100000.00, 'Berhasil'),
(6, 2, '2026-10-25', 500000.00, 'Berhasil');

--
-- Triggers `pembayaran`
--
DELIMITER $$
CREATE TRIGGER `trg_pembayaran_after_delete` AFTER DELETE ON `pembayaran` FOR EACH ROW BEGIN     DECLARE jumlah_terbayar DECIMAL(10,2) DEFAULT 0;     SELECT IFNULL(SUM(total_bayar), 0)     INTO jumlah_terbayar     FROM pembayaran     WHERE id_pemesanan = OLD.id_pemesanan       AND status_transaksi = 'Berhasil';     UPDATE pemesanan     SET status_pelunasan =         CASE             WHEN jumlah_terbayar >= total_biaya THEN 'Lunas'             ELSE 'Belum Lunas'         END     WHERE id_pemesanan = OLD.id_pemesanan;  END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_pembayaran_after_insert` AFTER INSERT ON `pembayaran` FOR EACH ROW BEGIN     DECLARE jumlah_terbayar DECIMAL(10,2) DEFAULT 0;     SELECT IFNULL(SUM(p.total_bayar), 0)     INTO jumlah_terbayar     FROM pembayaran AS p     WHERE p.id_pemesanan = NEW.id_pemesanan       AND p.status_transaksi = 'Berhasil'; UPDATE pemesanan     SET status_pelunasan =         CASE             WHEN jumlah_terbayar >= total_biaya THEN 'Lunas'             ELSE 'Belum Lunas'         END     WHERE id_pemesanan = NEW.id_pemesanan;  END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_pembayaran_after_update` AFTER UPDATE ON `pembayaran` FOR EACH ROW BEGIN     DECLARE jumlah_terbayar DECIMAL(10,2) DEFAULT 0;     INSERT INTO log_perubahan_pembayaran (         id_pembayaran,         total_bayar_lama,         total_bayar_baru,         status_lama,         status_baru     )     VALUES (         OLD.id_pembayaran,         OLD.total_bayar,         NEW.total_bayar,         OLD.status_transaksi,         NEW.status_transaksi     );     SELECT IFNULL(SUM(total_bayar), 0)     INTO jumlah_terbayar     FROM pembayaran     WHERE id_pemesanan = OLD.id_pemesanan       AND status_transaksi = 'Berhasil';     UPDATE pemesanan     SET status_pelunasan =         CASE             WHEN jumlah_terbayar >= total_biaya THEN 'Lunas'             ELSE 'Belum Lunas'         END     WHERE id_pemesanan = OLD.id_pemesanan;     IF NEW.id_pemesanan <> OLD.id_pemesanan THEN          SELECT IFNULL(SUM(total_bayar), 0)     INTO jumlah_terbayar         FROM pembayaran         WHERE id_pemesanan = NEW.id_pemesanan           AND status_transaksi = 'Berhasil';     UPDATE pemesanan         SET status_pelunasan =             CASE                 WHEN jumlah_terbayar >= total_biaya THEN 'Lunas'                 ELSE 'Belum Lunas'             END     WHERE id_pemesanan = NEW.id_pemesanan;      END IF;  END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `pemesanan`
--

CREATE TABLE `pemesanan` (
  `id_pemesanan` int NOT NULL,
  `nama_pelanggan` varchar(100) NOT NULL,
  `nama_kegiatan` varchar(100) NOT NULL,
  `lokasi_kegiatan` varchar(100) NOT NULL,
  `tanggal_pemesanan` date NOT NULL,
  `waktu_kegiatan` time NOT NULL,
  `total_biaya` decimal(10,2) NOT NULL DEFAULT '0.00',
  `status_pelunasan` varchar(20) NOT NULL DEFAULT 'Belum Lunas'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `pemesanan`
--

INSERT INTO `pemesanan` (`id_pemesanan`, `nama_pelanggan`, `nama_kegiatan`, `lokasi_kegiatan`, `tanggal_pemesanan`, `waktu_kegiatan`, `total_biaya`, `status_pelunasan`) VALUES
(1, 'Ketua DEMA', 'Seminar Nasional Teknologi', 'Hall Lt. 4 Gedung Utama', '2026-05-01', '08:00:00', 500000.00, 'Lunas'),
(2, 'Ketua UKM Taekwondo', 'Perfotoan UKM', 'Lantai 5 Gedung Utama', '2026-05-10', '19:00:00', 2000000.00, 'Belum Lunas'),
(3, 'Ketua HMP TI', 'Workshop UI/UX Design', 'Lab TI Lt. 1', '2026-06-25', '09:00:00', 750000.00, 'Lunas'),
(4, 'Ketua HMP Farmasi', 'Seminar Nasional Teknologi', 'Hall Lt. 4 Gedung Utama', '2026-07-01', '13:00:00', 1000000.00, 'Lunas'),
(5, 'Ketua Cerdas Cermat', 'Lomba Cerdas Cermat 2026', 'Gedung Terpadu', '2026-08-17', '07:00:00', 100000.00, 'Lunas');

--
-- Triggers `pemesanan`
--
DELIMITER $$
CREATE TRIGGER `trg_pemesanan_before_update` BEFORE UPDATE ON `pemesanan` FOR EACH ROW BEGIN     IF OLD.total_biaya <> NEW.total_biaya THEN         SET NEW.status_pelunasan = CASE             WHEN COALESCE((                 SELECT SUM(total_bayar)                 FROM pembayaran                 WHERE id_pemesanan = NEW.id_pemesanan                   AND status_transaksi = 'Berhasil'             ), 0) >= NEW.total_biaya             THEN 'Lunas'             ELSE 'Belum Lunas'         END;      END IF; END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `tim_multimedia`
--

CREATE TABLE `tim_multimedia` (
  `id_tim` int NOT NULL,
  `nama` varchar(100) NOT NULL,
  `divisi` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tim_multimedia`
--

INSERT INTO `tim_multimedia` (`id_tim`, `nama`, `divisi`) VALUES
(1, 'Haidar Rofiqi', 'Tim Fotografi'),
(2, 'Hafisulla', 'Tim Fotografi'),
(3, 'Hafiz Rahman', 'Tim Fotografi'),
(4, 'Haydar Husein', 'Tim Videografi'),
(5, 'Abdad Rukhuz', 'Tim Videografi'),
(6, 'Idris Efendi', 'Tim Broadcast'),
(7, 'Ahmad Samsu', 'Tim Broadcast'),
(8, 'Fajar Miftah', 'Tim Broadcast'),
(9, 'Raffa Ervansyah', 'Tim Visual'),
(10, 'Azka Masyail', 'Tim Visual');

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_ringkasan_pembayaran`
-- (See below for the actual view)
--
CREATE TABLE `v_ringkasan_pembayaran` (
`id_pemesanan` int
,`nama_kegiatan` varchar(100)
,`nama_pelanggan` varchar(100)
,`sisa_pembayaran` decimal(33,2)
,`status_pelunasan` varchar(20)
,`total_biaya` decimal(10,2)
,`total_terbayar` decimal(32,2)
);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `hasil_dokumentasi`
--
ALTER TABLE `hasil_dokumentasi`
  ADD PRIMARY KEY (`id_dokumentasi`),
  ADD KEY `fk_dokumentasi_pemesanan` (`id_pemesanan`);

--
-- Indexes for table `jadwal`
--
ALTER TABLE `jadwal`
  ADD PRIMARY KEY (`id_jadwal`),
  ADD KEY `fk_jadwal_pemesanan` (`id_pemesanan`),
  ADD KEY `fk_jadwal_tim` (`id_tim`);

--
-- Indexes for table `log_perubahan_pembayaran`
--
ALTER TABLE `log_perubahan_pembayaran`
  ADD PRIMARY KEY (`id_log`);

--
-- Indexes for table `pembayaran`
--
ALTER TABLE `pembayaran`
  ADD PRIMARY KEY (`id_pembayaran`),
  ADD KEY `fk_pembayaran_pemesanan` (`id_pemesanan`);

--
-- Indexes for table `pemesanan`
--
ALTER TABLE `pemesanan`
  ADD PRIMARY KEY (`id_pemesanan`);

--
-- Indexes for table `tim_multimedia`
--
ALTER TABLE `tim_multimedia`
  ADD PRIMARY KEY (`id_tim`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `log_perubahan_pembayaran`
--
ALTER TABLE `log_perubahan_pembayaran`
  MODIFY `id_log` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `pembayaran`
--
ALTER TABLE `pembayaran`
  MODIFY `id_pembayaran` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

-- --------------------------------------------------------

--
-- Structure for view `v_ringkasan_pembayaran`
--
DROP TABLE IF EXISTS `v_ringkasan_pembayaran`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_ringkasan_pembayaran`  AS SELECT `p`.`id_pemesanan` AS `id_pemesanan`, `p`.`nama_pelanggan` AS `nama_pelanggan`, `p`.`nama_kegiatan` AS `nama_kegiatan`, `p`.`total_biaya` AS `total_biaya`, coalesce(sum((case when (`b`.`status_transaksi` = 'Berhasil') then `b`.`total_bayar` else 0 end)),0) AS `total_terbayar`, greatest((`p`.`total_biaya` - coalesce(sum((case when (`b`.`status_transaksi` = 'Berhasil') then `b`.`total_bayar` else 0 end)),0)),0) AS `sisa_pembayaran`, `p`.`status_pelunasan` AS `status_pelunasan` FROM (`pemesanan` `p` left join `pembayaran` `b` on((`p`.`id_pemesanan` = `b`.`id_pemesanan`))) GROUP BY `p`.`id_pemesanan`, `p`.`nama_pelanggan`, `p`.`nama_kegiatan`, `p`.`total_biaya`, `p`.`status_pelunasan` ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `hasil_dokumentasi`
--
ALTER TABLE `hasil_dokumentasi`
  ADD CONSTRAINT `fk_dokumentasi_pemesanan` FOREIGN KEY (`id_pemesanan`) REFERENCES `pemesanan` (`id_pemesanan`);

--
-- Constraints for table `jadwal`
--
ALTER TABLE `jadwal`
  ADD CONSTRAINT `fk_jadwal_pemesanan` FOREIGN KEY (`id_pemesanan`) REFERENCES `pemesanan` (`id_pemesanan`),
  ADD CONSTRAINT `fk_jadwal_tim` FOREIGN KEY (`id_tim`) REFERENCES `tim_multimedia` (`id_tim`);

--
-- Constraints for table `pembayaran`
--
ALTER TABLE `pembayaran`
  ADD CONSTRAINT `fk_pembayaran_pemesanan` FOREIGN KEY (`id_pemesanan`) REFERENCES `pemesanan` (`id_pemesanan`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

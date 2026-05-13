// debug.rs -- Allocation Map Viewer
//
// Read-only diagnostic that renders the framebuffer as an ASCII grid
// showing pixel type distribution. Each cell is one character:
//
//   . = Empty (0x00000000)
//   C = Color (plain RGBA data)
//   B = BIOS (bit 31 set)
//   M = Mirror (alpha 0x7E)
//   T = Temporal (alpha 0x7D)
//   P = Portal (alpha 0x7C)
//   L = LogicGate (alpha 0x7B)
//   H = Hamming (alpha 0x7A)
//   G = Gradient (alpha 0x79)
//   ? = Unknown archetype
//
// Below the grid: a summary showing counts per type and the layer's
// allocation ratio (non-empty / total).

use crate::pixel::{self, PixelType};
use crate::render::Framebuffer;

/// Single-character glyph for each pixel type.
fn glyph(pt: &PixelType) -> char {
    match pt {
        PixelType::Color => 'C',
        PixelType::Bios => 'B',
        PixelType::Mirror => 'M',
        PixelType::Temporal => 'T',
        PixelType::Portal => 'P',
        PixelType::LogicGate => 'L',
        PixelType::Hamming => 'H',
        PixelType::Gradient => 'G',
    }
}

/// Per-type counters collected during a scan.
#[derive(Default)]
pub struct TypeCounts {
    pub empty: usize,
    pub color: usize,
    pub bios: usize,
    pub mirror: usize,
    pub temporal: usize,
    pub portal: usize,
    pub logic_gate: usize,
    pub hamming: usize,
    pub gradient: usize,
}

impl TypeCounts {
    fn inc(&mut self, pt: &PixelType) {
        match pt {
            PixelType::Color => self.color += 1,
            PixelType::Bios => self.bios += 1,
            PixelType::Mirror => self.mirror += 1,
            PixelType::Temporal => self.temporal += 1,
            PixelType::Portal => self.portal += 1,
            PixelType::LogicGate => self.logic_gate += 1,
            PixelType::Hamming => self.hamming += 1,
            PixelType::Gradient => self.gradient += 1,
        }
    }

    pub fn total(&self) -> usize {
        self.empty + self.color + self.bios + self.mirror
            + self.temporal + self.portal + self.logic_gate
            + self.hamming + self.gradient
    }

    pub fn allocated(&self) -> usize {
        self.total() - self.empty
    }
}

/// Render the framebuffer's active layer as an ASCII allocation map.
/// Returns the map string plus type counts.
pub fn allocation_map(fb: &Framebuffer) -> (String, TypeCounts) {
    let mut counts = TypeCounts::default();
    let mut rows = Vec::with_capacity(fb.height);

    for y in 0..fb.height {
        let mut row = String::with_capacity(fb.width);
        for x in 0..fb.width {
            let raw = fb.get(x, y);
            if raw == 0 {
                row.push('.');
                counts.empty += 1;
            } else {
                let pt = pixel::classify(raw);
                row.push(glyph(&pt));
                counts.inc(&pt);
            }
        }
        rows.push(row);
    }

    let map = rows.join("\n");
    (map, counts)
}

/// Render a specific layer (0-3) as an ASCII allocation map.
pub fn allocation_map_layer(fb: &Framebuffer, layer: usize) -> (String, TypeCounts) {
    let saved = fb.active_layer;
    // We need to read a specific layer without mutating fb.
    // Build the map manually from fb.layers[layer].
    let layer_idx = layer.min(3);
    let mut counts = TypeCounts::default();
    let mut rows = Vec::with_capacity(fb.height);

    for y in 0..fb.height {
        let mut row = String::with_capacity(fb.width);
        for x in 0..fb.width {
            let raw = fb.get_at_layer(x, y, layer_idx);
            if raw == 0 {
                row.push('.');
                counts.empty += 1;
            } else {
                let pt = pixel::classify(raw);
                row.push(glyph(&pt));
                counts.inc(&pt);
            }
        }
        rows.push(row);
    }

    let map = rows.join("\n");
    let _ = saved; // suppress unused warning
    (map, counts)
}

/// Format the full diagnostic: map grid + summary statistics.
pub fn render_diagnostic(fb: &Framebuffer) -> String {
    let (map, counts) = allocation_map(fb);
    let total = counts.total();
    let allocated = counts.allocated();
    let pct = if total > 0 {
        (allocated as f64 / total as f64) * 100.0
    } else {
        0.0
    };

    let mut out = String::new();
    out.push_str(&format!(
        "Allocation Map ({}x{}, layer {})\n",
        fb.width, fb.height, fb.active_layer
    ));
    out.push_str(&map);
    out.push_str(&format!(
        "\n\nAllocated: {}/{} ({:.1}%)\n",
        allocated, total, pct
    ));
    out.push_str(&format!(
        "  Color:{} Bios:{} Mirror:{} Temporal:{} Portal:{} Gate:{} Hamming:{} Gradient:{}\n",
        counts.color,
        counts.bios,
        counts.mirror,
        counts.temporal,
        counts.portal,
        counts.logic_gate,
        counts.hamming,
        counts.gradient,
    ));

    out
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::pixel;

    #[test]
    fn test_empty_framebuffer() {
        let fb = Framebuffer::new(4, 4);
        let (map, counts) = allocation_map(&fb);
        assert_eq!(map, "....\n....\n....\n....");
        assert_eq!(counts.empty, 16);
        assert_eq!(counts.allocated(), 0);
    }

    #[test]
    fn test_mixed_types() {
        let mut fb = Framebuffer::new(4, 2);
        fb.set(0, 0, pixel::rgb(0xFF, 0, 0)); // Color
        fb.set(1, 0, pixel::bios(1, 1, 0, 60)); // BIOS
        fb.set(2, 0, pixel::mirror(0, 0)); // Mirror
        fb.set(3, 0, pixel::temporal(200, 50)); // Temporal
        fb.set(0, 1, pixel::portal(0x1000)); // Portal
        fb.set(1, 1, pixel::hamming(0x12345)); // Hamming
        fb.set(2, 1, pixel::gradient(1, -1, 128)); // Gradient
        // (3,1) left empty

        let (map, counts) = allocation_map(&fb);
        assert_eq!(map, "CBMT\nPHG.");
        assert_eq!(counts.empty, 1);
        assert_eq!(counts.color, 1);
        assert_eq!(counts.bios, 1);
        assert_eq!(counts.mirror, 1);
        assert_eq!(counts.temporal, 1);
        assert_eq!(counts.portal, 1);
        assert_eq!(counts.hamming, 1);
        assert_eq!(counts.gradient, 1);
        assert_eq!(counts.allocated(), 7);
    }

    #[test]
    fn test_logic_gate_in_map() {
        use crate::logic::{GateType, LogicGate};
        let mut fb = Framebuffer::new(4, 4);
        // Place a logic gate at (1, 1)
        let gate_px = LogicGate::encode(0x7B, GateType::And, (-1, 0), (1, 0), 19);
        fb.set(1, 1, gate_px);

        let (map, counts) = allocation_map(&fb);
        let rows: Vec<&str> = map.split('\n').collect();
        assert_eq!(rows[1].chars().nth(1).unwrap(), 'L');
        assert_eq!(counts.logic_gate, 1);
    }

    #[test]
    fn test_allocation_ratio() {
        let mut fb = Framebuffer::new(10, 10); // 100 cells
        for x in 0..10 {
            fb.set(x, 0, pixel::rgb(x as u8 + 1, 0, 0)); // +1 to avoid zero
        }
        let (_, counts) = allocation_map(&fb);
        assert_eq!(counts.allocated(), 10);
        assert_eq!(counts.empty, 90);
    }

    #[test]
    fn test_layer_specific_map() {
        let mut fb = Framebuffer::new(4, 1);
        // Layer 0: a color pixel
        fb.set(0, 0, pixel::rgb(0xFF, 0, 0));
        // Switch to layer 1, put a different type
        fb.active_layer = 1;
        fb.set(1, 0, pixel::mirror(2, 3));

        // Check layer 0 map
        let (map0, c0) = allocation_map_layer(&fb, 0);
        assert_eq!(map0, "C...");
        assert_eq!(c0.color, 1);

        // Check layer 1 map
        let (map1, c1) = allocation_map_layer(&fb, 1);
        assert_eq!(map1, ".M..");
        assert_eq!(c1.mirror, 1);
    }

    #[test]
    fn test_diagnostic_format() {
        let mut fb = Framebuffer::new(2, 2);
        fb.set(0, 0, pixel::rgb(0xFF, 0, 0));
        let diag = render_diagnostic(&fb);
        assert!(diag.contains("C."));
        assert!(diag.contains("Allocated: 1/4"));
    }
}
